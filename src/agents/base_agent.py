from abc import ABC, abstractmethod

from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import AgentRole, DebateState
from src.prompts.action_prompts import ActionPrompts


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

    def introduce_topic(self, state: DebateState) -> str:
        """
        The agent will give the introducing argument for the debate topic.
        """
        if not state or "topic" not in state or not self.system_prompt:
            raise ValueError("Invalid state or system prompt.")

        context = ActionPrompts.create_introduction_prompt().format(
            system_prompt=self.system_prompt,
            role=self.role.value,
            topic=state["topic"]
        )
        return self.llm.invoke(context)


    def create_strategy(self, state: DebateState) -> str:
        """
        The agent will create a strategy based on the current state of the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")

        context = ActionPrompts.create_strategy_prompt().format(
            system_prompt=self.system_prompt,
            role=self.role.value,
            messages=state["messages"]
        )
        return self.llm.invoke(context)

    def create_argument(self, state: DebateState) -> str:
        """
        The agent will create an argument based on the current state of the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")

        context = ActionPrompts.create_argument_template().format(
            system_prompt=self.system_prompt,
            role=self.role.value,
            messages=state["messages"]
        )
        return self.llm.invoke(context)

    
    def conclude_debate(self, state: DebateState) -> str:
        """
        The agent will conclude the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")

        context = ActionPrompts.create_conclude_prompt().format(
            system_prompt=self.system_prompt,
            role=self.role.value,
            messages=state["messages"]
        )
        return self.llm.invoke(context)

    def get_name(self) -> str:
        return self.name

    def get_role(self) -> AgentRole:
        return self.role

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, role={self.role})"
