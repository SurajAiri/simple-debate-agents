from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import AgentRole, DebateState
from src.prompts.action_prompts import ActionPrompts
from src.prompts.agent_prompts import JUDGE_AGENT_SYSTEM_PROMPT

from .base_agent import DebateBaseAgent


class JudgeAgent(DebateBaseAgent):
    """
    Judge Agent for the debate.
    This agent is responsible for evaluating the arguments and providing feedback.
    """

    def __init__(
        self,
        llm: BaseLanguageModel,
        config: AgentConfig = AgentConfig(
            name="Judge",
            role=AgentRole.JUDGE,
            system_prompt=JUDGE_AGENT_SYSTEM_PROMPT,
        ),
    ):
        super().__init__(config, llm)

    def judge_and_conclude(self, state: DebateState) -> str:
        context = ActionPrompts.judge_and_conclude_prompt().format(
            system_prompt=self.system_prompt, messages=state["messages"]
        )
        return self.llm.invoke(context).content

    def introduce_topic(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot introduce topics")

    def create_strategy(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot create strategy introductions")

    def create_argument(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot create arguments")

    def conclude_debate(self, state: DebateState) -> str:
        raise NotImplementedError("Judge agent cannot conclude debates")
