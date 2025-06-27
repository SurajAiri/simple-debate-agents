# Multi-Agent with Strategic Debate System

## Overview

The Strategic Debate System extends the foundational Multi-Agents Simple Debate Graph Architecture with advanced strategic capabilities, enabling agents to formulate hidden strategies, employ psychological tactics, and engage in sophisticated debate manipulation while maintaining factual integrity.

## Key Architectural Differences

### 1. Enhanced State Management

The strategic system extends the base `DebateState` with strategy storage:

```python
DebateState = {
    # Base state from simple system
    "topic": str,
    "messages": List[Tuple[str, str]],
    "current_turn": AgentRole,
    "current_step": int,
    "max_steps": int,
    
    # Strategic extensions
    "favor_strategy": str,      # Hidden strategy for Favor agent
    "against_strategy": str,    # Hidden strategy for Against agent
}
```

### 2. Dual Prompt Architecture

The strategic system implements a dual-prompt architecture through the `use_strategic_prompt` parameter:

- **Simple Mode**: Uses `ActionPrompts` for basic debate functionality
- **Strategic Mode**: Employs `StrategicActionPrompts` for advanced manipulation

## Strategic Graph Execution Flow

### 1. Extended Control Flow

The strategic debate follows an enhanced state machine pattern implemented in `StrategicDebateGraph`:

```
START → agent_turn_check → [favor_agent | against_agent] → debate_complete_check → [continue | judge_agent] → strategy_analysis → END
```

### 2. Strategic Phase Integration

Unlike the [simple system's three phases](architecture.md#3-phase-based-agent-behavior), the strategic system incorporates strategy formulation into each phase:

#### Strategy Formulation Phase (`current_step == 1`)
- **Both Agents**: Generate hidden strategies using `create_strategy_formulation_prompt()`
- **Strategy Storage**: Strategies stored in state for later reference but hidden from opponents
- **Opening Statements**: Delivered using `create_opening_prompt()` with strategy awareness

#### Strategic Argumentation Phase (`1 < current_step < max_steps`)
- **Multi-layered Response**: Uses `create_middle_argument_prompt()` for:
  - Defensive analysis and counter-arguments
  - Offensive advancement with new evidence
  - Psychological manipulation through fact-based framing
  - Strategic adaptation to opponent's revealed approach

#### Strategic Conclusion Phase (`current_step >= max_steps`)
- **Synthesis-focused**: Uses `create_conclusion_prompt()` for closure rather than new arguments
- **Judge Evaluation**: Enhanced evaluation using `create_judge_evaluation_prompt()`
- **Meta-analysis**: Additional `strategy_analysis` node reveals strategic elements

## Advanced Agent Intelligence

### 1. Strategic Agent Framework

All agents inherit the strategic capabilities from [`DebateBaseAgent`](../src/agents/base_agent.py) with strategic prompt integration:

```python
# Strategic mode activation
agent = FavorAgent(llm=llm, use_strategic_prompt=True)
```

### 2. Multi-layered Prompt Engineering

The [`StrategicActionPrompts`](../src/prompts/strategic_action_prompts.py) system provides sophisticated prompt templates:

#### Strategy Formulation
- **Psychological framing** of factual information
- **Strategic timing** of evidence presentation
- **Cognitive bias awareness** for persuasion
- **Anticipatory counter-arguments** preparation

#### Advanced Argumentation
- **Four-layer response strategy**:
  1. Defensive layer for counter-attacks
  2. Offensive layer for position advancement
  3. Psychological manipulation layer
  4. Strategic adaptation layer

#### Factual Integrity Constraints
- Mandatory factual accuracy checks
- Graceful handling of knowledge limitations
- Ethical manipulation boundaries

### 3. Enhanced Judge Intelligence

The [`JudgeAgent`](../src/agents/judge_agent.py) in strategic mode provides:

- **Enhanced Evaluation**: Using weighted criteria (Factual Accuracy 40%, Logical Reasoning 30%, Argument Quality 20%, Debate Conduct 10%)
- **Meta-analysis Capability**: `analyse_the_debate()` method reveals strategic effectiveness
- **Strategy Assessment**: Evaluation of hidden strategy execution

## Strategic Communication Architecture

### 1. Hidden Strategy Protocol

Unlike the [simple system's transparent communication](architecture.md#communication-architecture), the strategic system implements:

```python
# Strategy storage pattern
state[agent.role.value + "_strategy"] = agent.create_strategy(state)

# Strategy access in arguments
strategy = state.get(self.role.value + "_strategy", "")
```

### 2. Multi-dimensional Message Analysis

Strategic messages contain multiple analytical dimensions:
- **Surface content**: Apparent argument structure
- **Strategic intent**: Hidden manipulation techniques
- **Factual foundation**: Verifiable claims and evidence
- **Psychological framing**: Emotional and cognitive positioning

### 3. Advanced Context Propagation

Each strategic agent receives enhanced context:
- **Own hidden strategy** for consistency
- **Opponent's revealed patterns** for adaptation
- **Round-specific tactical guidance**
- **Factual integrity constraints**

## Psychological Manipulation Framework

### 1. Fact-based Manipulation Architecture

The strategic system implements ethical manipulation through:

```python
# Psychological manipulation constraints
- Frame facts to trigger cognitive biases in your favor
- Use opponent's concessions to build your case
- Create doubt about opponent's expertise or reasoning
- Strategic use of authoritative sources
- Emotional framing of factual information
```

### 2. Strategic Adaptation Mechanisms

- **Real-time strategy adjustment** based on opponent behavior
- **Trap setting** for anticipated arguments
- **Weakness exploitation** through logical inconsistency identification
- **Counter-manipulation** defense strategies

### 3. Ethical Boundaries

The system maintains strict ethical constraints:
- **No false information** generation
- **Factual accuracy validation** before claim presentation
- **Graceful limitation acknowledgment**
- **Reasonable appearance** while being strategically effective

## Meta-Analysis Architecture

### 1. Post-Debate Strategic Assessment

The strategic system includes a unique `strategy_analysis` node that provides:

```python
# Meta-analysis components
1. Strategy execution effectiveness analysis
2. Manipulation technique assessment
3. Factual integrity evaluation
4. Strategic interaction dynamics
5. Outcome correlation analysis
```

### 2. Strategy Revelation Framework

Unlike the simple system's immediate transparency, the strategic system reveals:
- **Hidden strategy effectiveness**
- **Unnoticed manipulation attempts**
- **Judge perception vs. reality gaps**
- **Strategic adaptation success rates**

## Performance and Quality Assurance

### 1. Strategic Validation Layer

Enhanced validation beyond the [simple system](architecture.md#quality-assurance-architecture):
- **Strategy coherence validation**
- **Factual manipulation boundary checking**
- **Psychological tactic appropriateness verification**
- **Strategic consistency monitoring**

### 2. Advanced Error Handling

Strategic-specific error management:
- **Strategy formulation failures**
- **Manipulation attempt backfires**
- **Factual accuracy violations**
- **Ethical boundary crossings**

### 3. Strategic Performance Metrics

Additional monitoring capabilities:
- **Strategy execution success rates**
- **Manipulation detection by judges**
- **Factual accuracy maintenance under pressure**
- **Strategic adaptation effectiveness**

## Security and Ethical Governance

### 1. Enhanced Behavior Constraints

Strategic system implements additional safeguards:
- **Manipulation technique auditing**
- **Factual accuracy enforcement**
- **Ethical boundary monitoring**
- **Strategy revelation controls**

### 2. Strategic Transparency Controls

Unlike the [simple system's full transparency](architecture.md#security-and-governance), strategic mode provides:
- **Controlled strategy revelation** timing
- **Judge awareness modulation**
- **Meta-analysis disclosure management**
- **Educational insight provision**

This strategic architecture provides a sophisticated framework for studying advanced debate tactics, psychological persuasion techniques, and strategic communication while maintaining ethical standards and factual integrity requirements.