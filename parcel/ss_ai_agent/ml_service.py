from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class MLResult:
    success: bool = True
    prediction: str = ""
    confidence: float = 0.0
    details: str = ""


class MLService:
    def __init__(self):
        pass

    def predict_code_context(self, code_snippet: str) -> MLResult:
        snippet_lower = code_snippet.lower()
        if "class " in snippet_lower or "def " in snippet_lower:
            return MLResult(success=True, prediction="Python Core Logic", confidence=0.92, details="Core logic definition")
        elif "import " in snippet_lower or "#include" in snippet_lower:
            return MLResult(success=True, prediction="Dependency Imports", confidence=0.95, details="Module imports")
        elif "select " in snippet_lower or "insert " in snippet_lower:
            return MLResult(success=True, prediction="SQL Query", confidence=0.88, details="Database interaction")
        else:
            return MLResult(success=True, prediction="General Scripting", confidence=0.75, details="Generic code snippet")

    def analyze_style_ml(self, code: str) -> MLResult:
        issues = []
        if "\t" in code:
            issues.append("Tab characters detected (Use 4 spaces for PEP8)")
        if len(code.splitlines()) > 500:
            issues.append("High file length (>500 lines)")

        if issues:
            return MLResult(success=True, prediction="Style Violations Found", confidence=0.85, details="; ".join(issues))
        return MLResult(success=True, prediction="Clean PEP8 / SSQLM Style", confidence=0.98, details="No obvious style issues")

    def predict_bug_risk(self, code: str) -> MLResult:
        risk_score = 0.0
        details = []

        if "eval(" in code or "exec(" in code:
            risk_score += 0.5
            details.append("Dynamic evaluation usage")

        if "except:" in code or "except Exception: pass" in code:
            risk_score += 0.3
            details.append("Bare except or swallowed exception")

        confidence = min(1.0, 0.5 + risk_score)
        risk_level = "HIGH RISK" if risk_score >= 0.5 else ("MEDIUM RISK" if risk_score >= 0.2 else "LOW RISK")

        return MLResult(
            success=True,
            prediction=risk_level,
            confidence=confidence,
            details=", ".join(details) if details else "No immediate high risk patterns"
        )
