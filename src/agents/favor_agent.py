from base_agent import DebateBaseAgent
from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import DebateState


class FavorAgent(DebateBaseAgent):
    """
    Favor agent class that extends the DebateBaseAgent.
    This agent is responsible for favoring a position in the debate.
    """
    def __init__(self, config: AgentConfig, llm: BaseLanguageModel):
        super().__init__(config, llm)
