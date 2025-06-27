from base_agent import DebateBaseAgent
from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import DebateState


class AgainstAgent(DebateBaseAgent):
    """
    Against agent class that extends the DebateBaseAgent.
    This agent is responsible for opposing a position in the debate.
    """

    def __init__(self, config: AgentConfig, llm: BaseLanguageModel):
        super().__init__(config, llm)

    def create_strategy(self, state: DebateState) -> str:
        context = self.system_prompt + "\n"
        context += "You have to create a strategy for the debate.\n"
        context += "Current state: " + str(state['messages'])
        return self.llm.invoke(context)