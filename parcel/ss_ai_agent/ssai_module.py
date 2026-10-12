import os
from dataclasses import dataclass
from typing import Optional
from parcel.ss_ai_agent.local_agent import LocalAgent, AgentResponse
from parcel.ss_ai_agent.ml_service import MLService
from parcel.ss_ai_agent.web_search import WebSearchService
from parcel.ss_ai_agent.file_patcher import FilePatcher

@dataclass
class SSAIResponse:
    type: str = "MESSAGE"  # MESSAGE, ACTION, ERROR
    message: str = ""
    action_type: str = ""
    target_file: str = ""


class SSAIModule:
    def __init__(self, project_root: str = ""):
        self.project_root = project_root
        self.current_file = ""

        qlm_dir = os.path.join(project_root, "QLM") if project_root else "QLM"
        ssqlm_dir = os.path.join(project_root, "SS QLM") if project_root else "SS QLM"

        self.local_agent = LocalAgent(qlm_dir, ssqlm_dir)
        self.ml_service = MLService()
        self.web_search = WebSearchService()

        if project_root:
            self.local_agent.index_project(project_root)

    def process_instruction(self, instruction: str) -> SSAIResponse:
        agent_res: AgentResponse = self.local_agent.process(instruction)
        if agent_res.handled:
            return SSAIResponse(
                type="ACTION" if agent_res.action else "MESSAGE",
                message=agent_res.message,
                action_type=agent_res.action,
                target_file=agent_res.target
            )

        return SSAIResponse(
            type="MESSAGE",
            message=f"🤖 SSAI AI Orchestrator: Instrução processada. '{instruction}'"
        )

    def request_full_build(self, path: str, content: str):
        return FilePatcher.reconstruct(path, content)

    def request_safe_create(self, path: str, content: str):
        return FilePatcher.safe_create(path, content)

    def request_surgical_patch(self, path: str, start: str, end: str, patch: str):
        return FilePatcher.patch(path, start, end, patch)

    def request_smart_append(self, path: str, content: str, marker: str):
        return FilePatcher.smart_append(path, content, marker)
