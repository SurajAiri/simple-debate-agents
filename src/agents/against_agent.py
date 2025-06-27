from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import AgentRole
from src.prompts.agent_prompts import AGAINST_AGENT_SYSTEM_PROMPT

from .base_agent import DebateBaseAgent


class AgainstAgent(DebateBaseAgent):
    """
    Against agent class that extends the DebateBaseAgent.
    This agent is responsible for opposing a position in the debate.
    """

    def __init__(
        self,
        llm: BaseLanguageModel,
        config: AgentConfig = AgentConfig(
            name="Against",
            role=AgentRole.AGAINST,
            system_prompt=AGAINST_AGENT_SYSTEM_PROMPT,
        ),
    ):
        super().__init__(config, llm)
