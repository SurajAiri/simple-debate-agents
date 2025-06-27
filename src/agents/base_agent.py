from abc import ABC, abstractmethod

from langchain_core.language_models import BaseLanguageModel

from src.models.agent_config import AgentConfig
from src.models.debate_state import AgentRole
from src.models.debate_state import DebateState


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

        context = self.system_prompt + "\n"
        context += "You have to give the introduction to the debate topic.\n"
        context += "Topic: " + state["topic"]
        context += (
            "\nYou are a "
            + self.role.value
            + " agent.\n"
            + "And you have to give your introducing argument."
        )
        context += "It should not be more than 100 words."
        return self.llm.invoke(context)

    @abstractmethod
    def create_strategy(self, state: DebateState) -> str:
        pass

    def create_argument(self, state: DebateState) -> str:
        """
        The agent will create an argument based on the current state of the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")

        context = self.system_prompt + "\n"
        context += "You have to create an argument for the debate.\n"
        context += "Current state: " + str(state["messages"])
        context += (
            "\nYou are a "
            + self.role.value
            + " agent.\n"
            + "And you have to create your argument, defend your position, or refute the opponent's argument."
            + "\n It should not be more than 200 words."
        )
        return self.llm.invoke(context)

    
    def conclude_debate(self, state: DebateState) -> str:
        """
        The agent will conclude the debate.
        """
        if not state or "messages" not in state:
            raise ValueError("Invalid state.")

        context = self.system_prompt + "\n"
        context += "You have to conclude the debate.\n"
        context += "Current state: " + str(state["messages"])
        context += (
            "\nYou are a "
            + self.role.value
            + " agent.\n"
            + "And you have to conclude the debate."
            + "\n It should not be more than 150 words."
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
