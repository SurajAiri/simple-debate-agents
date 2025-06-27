from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

from src.agents import AgainstAgent, DebateBaseAgent, FavorAgent, JudgeAgent
from src.models.debate_state import AgentRole, DebateState


def perform_action(state: DebateState, agent: DebateBaseAgent) -> str:
    """
    Perform the action based on the current turn.
    """
    if state["current_step"] == 1:
        # first turn, introduce the topic and create strategies
        return agent.introduce_topic(state)
    if state["current_step"] < state["max_steps"]:
        # in-between turns, create arguments
        return agent.create_argument(state)
    # last turn, conclude the debate
    return agent.conclude_debate(state)


def favor_agent(state: DebateState) -> DebateState:
    """
    Favor the agent based on the current turn.
    """
    # turn is for favor (first talks)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        max_output_tokens=1024,
        temperature=0.5,
    )

    state["messages"].append(("Favor", perform_action(state, FavorAgent(llm=llm))))

    state["current_turn"] = AgentRole.AGAINST

    return state


def against_agent(state: DebateState) -> DebateState:
    """
    Against agent's turn.
    """
    # turn is for against (second talks)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        max_output_tokens=1024,
        temperature=0.5,
    )
    state["messages"].append(("Against", perform_action(state, AgainstAgent(llm=llm))))

    state["current_turn"] = AgentRole.FAVOR
    state["current_step"] += 1

    return state


def judge_agent(state: DebateState) -> DebateState:
    """
    Judge agent's turn.
    This is a placeholder for the judge agent logic.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        max_output_tokens=1024,
        temperature=0.5,
    )
    state["messages"].append(("Judge", JudgeAgent(llm=llm).judge_and_conclude(state)))

    return state


# conditional edges
def is_favor_turn(state: DebateState) -> bool:
    return state["current_turn"] == AgentRole.FAVOR


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

# visualize the graph
# from IPython.display import display, Image
# display(Image(app.get_graph().draw_mermaid_png()))

res = app.invoke(
    {
        "topic": "Is AI beneficial for society?",
        "favor_strategy": "",
        "against_strategy": "",
        "messages": [],
        "current_turn": AgentRole.FAVOR,
        "current_step": 1,
        "max_steps": 3,
    }
)

# print(res['messages'])
for message in res["messages"]:
    print(f"{message[0]}: {message[1]}")
