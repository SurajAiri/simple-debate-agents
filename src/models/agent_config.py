from pydantic import BaseModel

from src.models.debate_state import AgentRole


class AgentConfig(BaseModel):
    name: str
    role: AgentRole
    system_prompt: str = ""
    use_strategic_prompt: bool = False
