# debate/debate_state.py
from enum import Enum
from typing import Annotated, TypedDict


class AgentRole(Enum):
    FAVOR = "favor"
    AGAINST = "against"
    JUDGE = "judge"


class DebateState(TypedDict):
    topic: str
    favor_strategy: str
    against_strategy: str
    messages: Annotated[list[tuple[str, str]], "List of messages in the debate"]
    current_turn: AgentRole
    current_step: int
    max_steps: int
