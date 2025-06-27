from src.graph.strategic_debate_graph import StrategicDebateGraph

if __name__ == "__main__":
    # Initialize the StrategicDebateGraph with verbose output
    debate_graph = StrategicDebateGraph(verbose=True, use_strategic_prompt=True)
    print("Starting the strategic debate...")

    # Run a debate on a specific topic
    result = debate_graph.run_debate("Is AI beneficial for society?", max_steps=3,)

    # Print the results of the debate
    debate_graph.print_debate(result)
