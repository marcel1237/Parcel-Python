import os
import json
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class QLMMatch:
    matched: bool = False
    intent: str = ""
    response: str = ""
    action: str = ""
    mode: str = ""
    hint: str = ""


class QLMEngine:
    def __init__(self, rules_dir: str):
        self.rules_dir = rules_dir
        self.rules: List[dict] = []
        self.reload_rules()

    def reload_rules(self):
        self.rules.clear()
        if not os.path.exists(self.rules_dir):
            return

        for file_name in os.listdir(self.rules_dir):
            if file_name.endswith(".json"):
                full_path = os.path.join(self.rules_dir, file_name)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            self.rules.append(data)
                except Exception:
                    pass

    def find_match(self, instruction: str) -> QLMMatch:
        lower = instruction.lower()
        result = QLMMatch()

        for config in self.rules:
            rules_list = config.get("rules") or config.get("intents") or config.get("entries") or []
            for item in rules_list:
                triggers = item.get("trigger") or item.get("patterns") or []
                if not triggers:
                    if "pattern" in item:
                        triggers = [item["pattern"]]
                    elif "capability" in item:
                        triggers = [item["capability"]]
                    elif "target" in item:
                        triggers = [item["target"]]

                for pattern in triggers:
                    pattern_str = str(pattern)
                    matched = False

                    if pattern_str.startswith("^") or ".*" in pattern_str or "\\b" in pattern_str:
                        try:
                            matched = bool(re.search(pattern_str, lower, re.IGNORECASE))
                        except Exception:
                            matched = pattern_str.lower() in lower
                    else:
                        matched = pattern_str.lower() in lower

                    if matched:
                        result.matched = True
                        result.intent = item.get("intent") or item.get("capability") or item.get("blueprint") or item.get("utility") or ""

                        if "response" in item:
                            result.response = item["response"]
                        elif "logic" in item:
                            result.response = item["logic"]
                        elif "value" in item:
                            result.response = item["value"]
                        elif "rationale" in item:
                            result.response = item["rationale"]
                        elif "reason" in item:
                            result.response = f"Regra: {item['reason']} (Status: {item.get('status', '')})"

                        result.action = item.get("action", "")
                        if not result.action and "implementation" in item:
                            result.action = "CODE_SAMPLE"
                            result.mode = item["implementation"]
                        if not result.action and "use_instead" in item:
                            result.action = f"SUGGESTION: {item['use_instead']}"

                        result.mode = item.get("mode") or item.get("implementation") or ""
                        result.hint = item.get("hint", result.response)
                        return result

        return result

    @staticmethod
    def extract_filename(instruction: str) -> str:
        match = re.search(r"\b\w+\.(sh|cpp|hpp|py|json|txt|xml)\b", instruction)
        return match.group(0) if match else ""
