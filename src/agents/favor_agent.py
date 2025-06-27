from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import AgentRole
from src.prompts.agent_prompts import FAVOR_AGENT_SYSTEM_PROMPT

from .base_agent import DebateBaseAgent


class FavorAgent(DebateBaseAgent):
    """
    Favor agent class that extends the DebateBaseAgent.
    This agent is responsible for favoring a position in the debate.
    """

    def __init__(
        self,
        llm: BaseLanguageModel,
        config: AgentConfig = AgentConfig(
            name="Favor", role=AgentRole.FAVOR, system_prompt=FAVOR_AGENT_SYSTEM_PROMPT
        ),
        use_strategic_prompt: bool = False,
    ):
        super().__init__(config, llm, use_strategic_prompt=use_strategic_prompt)
