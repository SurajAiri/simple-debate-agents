# flake8: noqa
import textwrap


def print_debate(result: dict):
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
