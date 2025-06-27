from abc import ABC, abstractmethod

from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import AgentRole, DebateState
from src.prompts.action_prompts import ActionPrompts
from src.prompts.strategic_action_prompts import StrategicActionPrompts


class DebateBaseAgent(ABC):
    """
    Base class for debate agents.
    """

    # task -> introduce, create strategies, create arguments, conclude

    def __init__(self, config: AgentConfig, llm: BaseLanguageModel):
        self.name = config.name
        self.role = config.role
        self.system_prompt = config.system_prompt
        self.llm = llm
        self.use_strategic_prompt = config.use_strategic_prompt

    def introduce_topic(self, state: DebateState) -> str:
        """
        The agent will give the introducing argument for the debate topic.
        """
        if not state or "topic" not in state or not self.system_prompt:
            raise ValueError("Invalid state or system prompt.")

        if self.use_strategic_prompt:
            strategy = state.get(self.role.value + "_strategy", "")
            print(f"Using strategy {self.role.value}_strategy: {strategy}")
            context = StrategicActionPrompts.create_opening_prompt().format(
                system_prompt=self.system_prompt,
                role=self.role.value,
                topic=state["topic"],
                strategy=strategy,
                total_rounds=state.get("max_steps", 3),
            )
        else:
            context = ActionPrompts.create_introduction_prompt().format(
                system_prompt=self.system_prompt,
                role=self.role.value,
                topic=state["topic"],
            )
        return self.llm.invoke(context).content

    def create_strategy(self, state: DebateState) -> str:
        """
        The agent will create a strategy based on the current state of the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")

        if self.use_strategic_prompt:
            strategy = state.get(self.role.value + "_strategy", "")
            print(f"Using strategy {self.role.value + '_strategy'}: {strategy}")
            context = (
                StrategicActionPrompts.create_strategy_formulation_prompt().format(
                    system_prompt=self.system_prompt,
                    role=self.role.value,
                    total_rounds=state.get("total_rounds", 3),
                    topic=state.get("topic", "No topic specified"),
                    position="In favor to topic"
                    if self.role == AgentRole.FAVOR
                    else "Against the topic",
                )
            )
        else:
            context = ActionPrompts.create_strategy_prompt().format(
                system_prompt=self.system_prompt,
                role=self.role.value,
                messages=state["messages"],
            )
        return self.llm.invoke(context).content

    def create_argument(self, state: DebateState) -> str:
        """
        The agent will create an argument based on the current state of the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")
        if self.use_strategic_prompt:
            strategy = state.get(self.role.value + "_strategy", "")
            print(f"Using strategy {self.role.value + '_strategy'}: {strategy}")
            context = StrategicActionPrompts.create_middle_argument_prompt().format(
                system_prompt=self.system_prompt,
                role=self.role.value,
                current_round=state['current_step'],
                total_rounds=state['max_steps'],
                strategy=strategy,
                opponent_last_argument=state['messages'][-1],
                messages=state["messages"][:-1],
                rounds_remaining=state.get("max_steps", 3) - state['current_step'],
            )
        else:
            context = ActionPrompts.create_argument_template().format(
                system_prompt=self.system_prompt,
                role=self.role.value,
                messages=state["messages"],
            )
        return self.llm.invoke(context).content

    def conclude_debate(self, state: DebateState) -> str:
        """
        The agent will conclude the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")

        if self.use_strategic_prompt:
            strategy = state.get(self.role.value + "_strategy", "")
            print(f"Using strategy {self.role.value + '_strategy'}: {strategy}")
            context = StrategicActionPrompts.create_conclusion_prompt().format(
                system_prompt=self.system_prompt,
                role=self.role.value,
                messages=state["messages"],
                strategy=strategy
            )
        else:
            context = ActionPrompts.create_conclude_prompt().format(
                system_prompt=self.system_prompt,
                role=self.role.value,
                messages=state["messages"],
            )
        return self.llm.invoke(context).content

    def get_name(self) -> str:
        return self.name

    def get_role(self) -> AgentRole:
        return self.role

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, role={self.role})"
