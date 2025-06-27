from enum import Enum
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class AgentTurn(Enum):
    FAVOR = "favor"
    AGAINST = "against"


class DebateState(TypedDict):
    """
    State for the debate graph.
    """

    topic: str
    agent1: str
    agent2: str
    messages: Annotated[list[tuple[str, str]], "List of messages in the debate"]
    current_turn: AgentTurn
    current_step: int
    max_steps: int


def favor_agent(state: DebateState) -> DebateState:
    """
    Favor the agent based on the current turn.
    """

    # turn is for favor (first talks)

    # if turn 0 -> intro and strategy creation
    # in-between turns -> argument creation
    # last turn -> conclusion
    if state["current_step"] == 1:
        # first turn, introduce the topic and create strategies
        state["messages"].append(
            ("Favor", "Favor agent introduces the topic and creates strategies.")
        )
    elif state["current_step"] < state["max_steps"]:
        # in-between turns, create arguments
        state["messages"].append(
            ("Favor", "Favor agent creates an argument." + str(state["current_step"]))
        )
    else:
        # last turn, conclude the debate
        state["messages"].append(("Favor", "Favor agent concludes the debate."))

    state["current_turn"] = AgentTurn.AGAINST

    return state


def against_agent(state: DebateState) -> DebateState:
    """
    Against agent's turn.
    """

    # turn is for against (second talks)

    # if turn 0 -> intro and strategy creation
    # in-between turns -> argument creation
    # last turn -> conclusion
    if state["current_step"] == 1:
        # first turn, introduce the topic and create strategies
        state["messages"].append(
            ("Against", "Against agent introduces the topic and creates strategies.")
        )
    elif state["current_step"] < state["max_steps"]:
        # in-between turns, create arguments
        state["messages"].append(
            (
                "Against",
                "Against agent creates an argument." + str(state["current_step"]),
            )
        )
    else:
        # last turn, conclude the debate
        state["messages"].append(("Against", "Against agent concludes the debate."))

    state["current_turn"] = AgentTurn.FAVOR
    state["current_step"] += 1

    return state


def judge_agent(state: DebateState) -> DebateState:
    """
    Judge agent's turn.
    This is a placeholder for the judge agent logic.
    """

    # judge logic can be added here
    state["messages"].append(("Judge", "Judge agent evaluates the debate."))

    return state


# conditional edges
def is_favor_turn(state: DebateState) -> bool:
    return state["current_turn"] == AgentTurn.FAVOR


def is_complete(state: DebateState) -> bool:
    return state["current_step"] > state["max_steps"]


graph = StateGraph(DebateState)

# add nodes
graph.add_node("favor_agent", favor_agent)
graph.add_node("against_agent", against_agent)
graph.add_node("judge_agent", judge_agent)
graph.add_node("agent_turn_check", lambda state: state)
graph.add_node("debate_complete_check", lambda state: state)


# add edges
graph.add_edge(START, "agent_turn_check")
graph.add_conditional_edges(
    "agent_turn_check", is_favor_turn, {True: "favor_agent", False: "against_agent"}
)
graph.add_conditional_edges(
    "debate_complete_check",
    is_complete,
    {True: "judge_agent", False: "agent_turn_check"},
)
graph.add_edge("favor_agent", "debate_complete_check")
graph.add_edge("against_agent", "debate_complete_check")
graph.add_edge("judge_agent", END)


# compile the graph
app = graph.compile()

# # visualize the graph
# from IPython.display import display, Image
# display(Image(app.get_graph().draw_mermaid_png()))

res = app.invoke(
    {
        "topic": "Climate Change",
        "agent1": "Alice",
        "agent2": "Bob",
        "messages": [],
        "current_turn": AgentTurn.FAVOR,
        "current_step": 1,
        "max_steps": 3,
    }
)

# print(res['messages'])
for message in res["messages"]:
    print(f"{message[0]}: {message[1]}")