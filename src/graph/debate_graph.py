import textwrap

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

from src.agents import AgainstAgent, DebateBaseAgent, FavorAgent, JudgeAgent
from src.models.debate_state import AgentRole, DebateState


class DebateGraph:
    def __init__(
        self,
        model_name: str = "gemini-1.5-flash",
        max_output_tokens: int = 1024,
        temperature: float = 0.5,
        verbose: bool = False,
    ):
        """
        Initialize the DebateGraph with configurable LLM parameters.
        """
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.app = self._build_graph()
        self.verbose = verbose


    def _create_llm(self):
        """Create and return a configured LLM instance."""
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            max_output_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )

    def _perform_action(self, state: DebateState, agent: DebateBaseAgent) -> str:
        """Perform the action based on the current turn."""
        if state["current_step"] == 1:
            return agent.introduce_topic(state)
        if state["current_step"] < state["max_steps"]:
            return agent.create_argument(state)
        return agent.conclude_debate(state)

    def _favor_agent(self, state: DebateState) -> DebateState:
        """Favor agent's turn."""
        llm = self._create_llm()
        state["messages"].append(
            ("Favor", self._perform_action(state, FavorAgent(llm=llm)))
        )
        state["current_turn"] = AgentRole.AGAINST

        if self.verbose:
            print(f"\033[92mFavor agent: {state['messages'][-1][1]}\033[0m")
        return state

    def _against_agent(self, state: DebateState) -> DebateState:
        """Against agent's turn."""
        llm = self._create_llm()
        state["messages"].append(
            ("Against", self._perform_action(state, AgainstAgent(llm=llm)))
        )
        state["current_turn"] = AgentRole.FAVOR
        state["current_step"] += 1

        if self.verbose:
            print(f"\033[92mAgainst agent: {state['messages'][-1][1]}\033[0m")
        return state

    def _judge_agent(self, state: DebateState) -> DebateState:
        """Judge agent's turn."""
        llm = self._create_llm()
        state["messages"].append(
            ("Judge", JudgeAgent(llm=llm).judge_and_conclude(state))
        )

        if self.verbose:
            print(f"\033[92mJudge agent: {state['messages'][-1][1]}\033[0m")
        return state

    def _is_favor_turn(self, state: DebateState) -> bool:
        """Check if it's favor agent's turn."""
        return state["current_turn"] == AgentRole.FAVOR

    def _is_complete(self, state: DebateState) -> bool:
        """Check if debate is complete."""
        return state["current_step"] > state["max_steps"]

    def _build_graph(self):
        """Build and compile the debate graph."""
        graph = StateGraph(DebateState)

        # Add nodes
        graph.add_node("favor_agent", self._favor_agent)
        graph.add_node("against_agent", self._against_agent)
        graph.add_node("judge_agent", self._judge_agent)
        graph.add_node("agent_turn_check", lambda state: state)
        graph.add_node("debate_complete_check", lambda state: state)

        # Add edges
        graph.add_edge(START, "agent_turn_check")
        graph.add_conditional_edges(
            "agent_turn_check",
            self._is_favor_turn,
            {True: "favor_agent", False: "against_agent"},
        )
        graph.add_conditional_edges(
            "debate_complete_check",
            self._is_complete,
            {True: "judge_agent", False: "agent_turn_check"},
        )
        graph.add_edge("favor_agent", "debate_complete_check")
        graph.add_edge("against_agent", "debate_complete_check")
        graph.add_edge("judge_agent", END)

        return graph.compile()

    def run_debate(self, topic: str, max_steps: int = 3) -> dict:
        """
        Run a debate on the given topic.

        Args:
            topic: The debate topic
            max_steps: Maximum number of debate rounds

        Returns:
            Dictionary containing the debate results
        """
        initial_state = {
            "topic": topic,
            "favor_strategy": "",
            "against_strategy": "",
            "messages": [],
            "current_turn": AgentRole.FAVOR,
            "current_step": 1,
            "max_steps": max_steps,
        }
        return self.app.invoke(initial_state)

    def print_debate(self, result: dict):
        """Print the debate messages in a formatted way with enhanced colors and styling."""
        # Enhanced color codes and styles
        colors = {
            "Favor": "\033[1;94m",      # Bold Blue
            "Against": "\033[1;93m",    # Bold Yellow  
            "Judge": "\033[1;92m",      # Bold Green
        }
        
        # Additional formatting codes
        BOLD = "\033[1m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"
        RESET = "\033[0m"
        BG_DARK = "\033[40m"
        BG_LIGHT = "\033[47m"
        
        # Print enhanced header
        print(f"\n{BOLD}{BG_DARK}{'='*80}{RESET}")
        print(f"{BOLD}{UNDERLINE}🏛️  DEBATE RESULTS: {result.get('topic', 'Unknown Topic')} 🏛️{RESET}")
        print(f"{BOLD}{BG_DARK}{'='*80}{RESET}\n")
        
        # Print debate messages with enhanced styling
        for i, (agent, message) in enumerate(result.get("messages", []), 1):
            agent_color = colors.get(agent, "\033[97m")  # White as fallback
            
            # Create agent-specific icons and styling
            if agent == "Favor":
                icon = "👍"
                border = "▶"
            elif agent == "Against":
                icon = "👎"
                border = "◀"
            else:  # Judge
                icon = "⚖️"
                border = "●"
                
            print(f"{agent_color}{BOLD}{border*3} {icon} {agent.upper()} AGENT #{i} {border*3}{RESET}")
            print(f"{agent_color}┌{'─'*76}┐{RESET}")
            
            # Word wrap the message for better readability
            wrapped_message = textwrap.fill(message, width=74)
            for line in wrapped_message.split('\n'):
                print(f"{agent_color}│ {line:<74} │{RESET}")
                
            print(f"{agent_color}└{'─'*76}┘{RESET}\n")
        
        # Print footer
        print(f"{BOLD}{BG_DARK}{'='*80}{RESET}")
        print(f"{ITALIC}💭 Total messages: {len(result.get('messages', []))} | Steps completed: {result.get('current_step', 0)}{RESET}")
        print(f"{BOLD}{BG_DARK}{'='*80}{RESET}\n")

    def get_graph(self):
        """Get the underlying graph for visualization or further manipulation."""
        return self.app.get_graph().draw_mermaid_png()


# Usage example
if __name__ == "__main__":
    debate_graph = DebateGraph(verbose=True)
    result = debate_graph.run_debate("Is AI beneficial for society?")
    debate_graph.print_debate(result)
