from base_agent import DebateBaseAgent
from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import DebateState
from src.prompts.action_prompts import ActionPrompts


class JudgeAgent(DebateBaseAgent):
    """
    Judge Agent for the debate.
    This agent is responsible for evaluating the arguments and providing feedback.
    """

    def __init__(self, config: AgentConfig, llm: BaseLanguageModel):
        super().__init__(config, llm)

    def judge_and_conclude(self, state: DebateState) -> str:
        context = ActionPrompts.judge_and_conclude_prompt().format(
            system_prompt=self.system_prompt,
            messages=state["messages"]
        )
        return self.llm.invoke(context)
    
    def introduce_topic(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot introduce topics")
    
    def create_strategy(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot create strategy introductions")

    def create_argument(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot create arguments")

    def conclude_debate(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot conclude debates")