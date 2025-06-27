from src.graph.debate_graph import DebateGraph

if __name__ == "__main__":
    # Initialize the DebateGraph with verbose output
    debate_graph = DebateGraph(verbose=False)
    
    # Run a debate on a specific topic
    result = debate_graph.run_debate("Is AI beneficial for society?")
    
    # Print the results of the debate
    debate_graph.print_debate(result)