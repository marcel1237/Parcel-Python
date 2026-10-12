import re
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    is_valid: bool = True
    output: str = "✓ Script passed SSQLM basic heuristics."
    error_count: int = 0


class ScriptValidator:
    @staticmethod
    def deep_audit(content: str) -> ValidationResult:
        result = ValidationResult()
        issues: List[str] = []

        if "eval " in content:
            issues.append("CRITICAL: 'eval' usage detected. Potential command injection vector.")

        if "> /tmp/" in content and "mktemp" not in content:
            issues.append("WARNING: Direct write to /tmp detected without mktemp. Brittle and insecure.")

        if "trap " not in content and len(content) > 500:
            issues.append("ADVICE: Complex script detected without 'trap' for cleanup or error reporting.")

        if re.search(r"rm\s+-[a-zA-Z]*r[a-zA-Z]*\s+\$[^\{\"]", content):
            issues.append("CRITICAL: Unquoted variable in recursive 'rm'. SSQLM mandates quotes to prevent catastrophic data loss.")

        if re.search(r"(?:^|\s)\$([a-zA-Z_][a-zA-Z0-9_]*)(?![\"\}])", content) and "bash" in content:
            issues.append("ADVICE: Unquoted variable detected. Use \"$var\" to prevent word splitting and globbing (SSQLM standard).")

        if "sudo " in content:
            issues.append("WARNING: 'sudo' detected. SSQLM recommends delegating privilege escalation to the orchestrator.")

        if re.search(r"\w+\s*\(\)\s*\{", content) and "local " not in content:
            issues.append("ADVICE: Function detected but no 'local' variables found. SSQLM mandates scope isolation.")

        if issues:
            result.is_valid = False
            result.output = "\n".join(issues)
            result.error_count = len(issues)

        return result
