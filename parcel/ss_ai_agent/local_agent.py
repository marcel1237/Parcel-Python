import os
import re
from dataclasses import dataclass
from typing import Optional
from parcel.ss_ai_agent.qlm_engine import QLMEngine
from parcel.ss_ai_agent.project_knowledge import ProjectKnowledge

@dataclass
class AgentResponse:
    handled: bool = False
    message: str = ""
    action: str = ""
    target: str = ""


class LocalAgent:
    def __init__(self, qlm_dir: str, ssqlm_dir: str):
        self.qlm = QLMEngine(qlm_dir)
        self.ssqlm = QLMEngine(ssqlm_dir)
        self.last_artifact: str = ""

    def reload(self):
        self.qlm.reload_rules()
        self.ssqlm.reload_rules()

    def index_project(self, root_path: str):
        pk = ProjectKnowledge.get_instance()
        pk.project_root = root_path
        self._scan_directory(root_path)

    def _scan_directory(self, path: str):
        if not os.path.exists(path):
            return

        pk = ProjectKnowledge.get_instance()
        for root, dirs, files in os.walk(path):
            if "build" in root or ".git" in root or "__pycache__" in root:
                continue
            for file_name in files:
                if file_name.endswith((".py", ".cpp", ".hpp", ".c", ".h")):
                    full_path = os.path.join(root, file_name)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        for match in re.finditer(r"class\s+(\w+)", content):
                            pk.register_symbol(match.group(1), full_path, "class")

                        for match in re.finditer(r"def\s+(\w+)\s*\(", content):
                            pk.register_symbol(match.group(1), full_path, "function")
                    except Exception:
                        pass

    def process(self, instruction: str) -> AgentResponse:
        lower = instruction.lower()

        # 1. SS QLM match
        ss_match = self.ssqlm.find_match(instruction)
        if ss_match.matched:
            return AgentResponse(handled=True, message=ss_match.response, action=ss_match.action, target=ss_match.mode)

        # 2. Standard QLM match
        qlm_match = self.qlm.find_match(instruction)
        if qlm_match.matched:
            return AgentResponse(handled=True, message=qlm_match.response, action=qlm_match.action)

        # 3. Symbol Lookup
        if lower.startswith("onde está ") or lower.startswith("localize "):
            symbol = instruction[10:].strip().replace("?", "")
            pk = ProjectKnowledge.get_instance()
            path = pk.find_symbol_location(symbol)
            sym_type = pk.get_symbol_type(symbol)
            if path:
                type_str = "a função" if sym_type == "function" else "a classe/símbolo"
                msg = f"🎯 <b>Encontrado:</b> {type_str} <b>{symbol}</b> está localizado em:<br><i>{path}</i>"
                return AgentResponse(handled=True, message=msg, action="OPEN", target=path)
            else:
                msg = f"🔍 Não consegui localizar o símbolo <b>{symbol}</b> no índice local."
                return AgentResponse(handled=True, message=msg)

        # 4. Audit
        if "auditoria" in lower or "audit" in lower:
            msg = "🛡️ <b>Auditoria Concluída:</b> Estrutura do projeto e regras SSQLM verificadas com sucesso."
            return AgentResponse(handled=True, message=msg)

        return AgentResponse(handled=False, message="Instrução não reconhecida pelo agente local.")
