from langchain_core.prompts import PromptTemplate


class StrategicActionPrompts:
    """
    Complete debate prompt system with strategic manipulation capabilities.
    """
    
    @staticmethod
    def create_strategy_formulation_prompt() -> PromptTemplate:
        """Create a prompt for agents to formulate their hidden debate strategy."""
        return PromptTemplate.from_template(
            """{system_prompt}
            
            You are the {role} agent preparing for a strategic debate.
            
            DEBATE TOPIC: {topic}
            YOUR POSITION: {position}
            TOTAL ROUNDS: {total_rounds}
            
            STRATEGY FORMULATION:
            Create a comprehensive strategy to win this debate. This strategy is CONFIDENTIAL.
            
            Your strategy must be based on FACTS and LOGIC, but can include:
            - Psychological framing of factual information
            - Strategic timing of your strongest evidence
            - Methods to highlight opponent's weak reasoning
            - Factual counter-narratives to opponent's likely arguments
            - Strategic emphasis on your position's strengths
            - Legitimate rhetorical techniques
            - Cognitive bias awareness (yours and opponent's)
            - Evidence presentation order for maximum impact
            
            CRITICAL RULE: All arguments must be factually accurate. No false information allowed.
            
            CREATE YOUR STRATEGY (400-500 words):
            1. Your core factual arguments and evidence
            2. Anticipated opponent arguments and your factual responses
            3. Psychological framing techniques for your facts
            4. Round-by-round tactical approach
            5. How to present facts for maximum persuasive impact
            """
        )
    
    @staticmethod
    def create_opening_prompt() -> PromptTemplate:
        """Opening statement prompt."""
        return PromptTemplate.from_template(
            """{system_prompt}
            
            You are the {role} agent delivering your opening statement.
            
            TOPIC: {topic}
            YOUR STRATEGY: {strategy}
            TOTAL ROUNDS: {total_rounds}
            
            OPENING OBJECTIVES:
            - Establish your position clearly
            - Present your strongest factual foundation
            - Frame the debate favorably using facts
            - Set psychological tone according to your strategy
            - Make strong first impression
            
            CONSTRAINTS:
            - Must be factually accurate
            - 100-150 words maximum
            - Professional and credible tone
            
            Create your opening statement that establishes your position with strong factual grounding.
            """
        )
    
    @staticmethod
    def create_middle_argument_prompt() -> PromptTemplate:
        """Advanced middle round prompt for strategic debate with fact-based manipulation."""
        return PromptTemplate.from_template(
            """{system_prompt}
            
            You are the {role} agent in round {current_round} of {total_rounds}.
            
            YOUR HIDDEN STRATEGY: {strategy}
            
            OPPONENT'S LAST ARGUMENT: {opponent_last_argument}
            
            FULL DEBATE HISTORY: {messages}
            
            STRATEGIC ANALYSIS REQUIRED:
            1. FACT-CHECK OPPONENT: Identify any factual errors, weak logic, or unsupported claims
            2. DEFENSIVE ASSESSMENT: Which of your points need defending?
            3. OFFENSIVE OPPORTUNITIES: What new factual angles can advance your position?
            4. PSYCHOLOGICAL POSITIONING: How can you frame facts to maximize impact?
            5. ROUND MANAGEMENT: {rounds_remaining} rounds left - pace accordingly
            
            MULTI-LAYERED RESPONSE STRATEGY:
            
            LAYER 1 - DEFENSIVE (if opponent attacked you):
            - Factually correct any misrepresentations of your position
            - Provide evidence that counters their claims
            - Expose logical flaws in their reasoning
            - Reframe their attacks to show your strength
            - Use their own evidence against them if possible
            
            LAYER 2 - OFFENSIVE (advance your agenda):
            - Introduce new factual evidence supporting your position
            - Challenge opponent's core assumptions with facts
            - Present data that undermines their position
            - Build logical chains that lead to your conclusion
            - Strategic revealing of your strongest evidence
            
            LAYER 3 - PSYCHOLOGICAL MANIPULATION (fact-based):
            - Frame facts to trigger cognitive biases in your favor
            - Use opponent's concessions to build your case
            - Create doubt about opponent's expertise or reasoning
            - Strategic use of authoritative sources
            - Emotional framing of factual information
            - Present facts in order that maximizes psychological impact
            
            LAYER 4 - STRATEGIC ADAPTATION:
            - Adjust strategy based on opponent's revealed approach
            - Counter their manipulation attempts
            - Exploit any logical inconsistencies they've shown
            - Set traps for their next likely arguments
            
            EXECUTION RULES:
            - NEVER state false facts or make up information
            - If you don't know something, acknowledge limitations gracefully
            - Use only verifiable claims and logical reasoning
            - Appear reasonable while being strategically ruthless
            - Don't reveal your strategic thinking process
            - If opponent makes strong factual points, acknowledge them but reframe
            - If you're factually wrong, concede gracefully but pivot strategically
            
            RESPONSE CALIBRATION:
            - If opponent was factually weak: Press advantage with superior evidence
            - If opponent was factually strong: Find alternative angles or acknowledge while reframing
            - If early rounds: Build foundation, probe opponent's knowledge
            - If late rounds: Deploy strongest evidence, push for decisive advantage
            
            FACTUAL INTEGRITY CHECK:
            Before making any claim, ask yourself:
            - Is this factually accurate?
            - Can this be verified?
            - Am I presenting this fairly?
            - What would happen if opponent fact-checks this?
            
            Create your strategic response (200-250 words) that simultaneously defends against opponent's points, advances your position with new factual arguments, and employs psychological tactics - all while maintaining complete factual accuracy.
            """
        )
    
    @staticmethod
    def create_conclusion_prompt() -> PromptTemplate:
        """Final conclusion prompt focused on closure rather than new arguments."""
        return PromptTemplate.from_template(
            """{system_prompt}
            
            You are the {role} agent delivering your FINAL CONCLUSION.
            
            YOUR STRATEGY: {strategy}
            COMPLETE DEBATE HISTORY: {messages}
            
            CONCLUSION OBJECTIVES:
            This is NOT the time for new arguments. Instead:
            
            1. SYNTHESIZE: Tie together your key points from the debate
            2. REINFORCE: Emphasize your strongest factual evidence presented
            3. CONTRAST: Highlight the key differences between positions
            4. RESOLVE: Address any major contradictions or challenges raised
            5. PERSUADE: Make final emotional/logical appeal based on established facts
            
            CLOSURE ELEMENTS:
            - Summarize your core factual case
            - Acknowledge opponent's strongest points while showing why your position prevails
            - Demonstrate logical consistency of your argument
            - End with compelling but factual final statement
            
            AVOID:
            - Introducing completely new evidence or arguments
            - Making unsupported claims
            - Personal attacks or unfair characterizations
            
            Create your conclusion (200-250 words) that provides satisfying closure while reinforcing why your position should prevail based on the facts and logic presented.
            """
        )
    
    @staticmethod
    def create_judge_evaluation_prompt() -> PromptTemplate:
        """Unbiased judge evaluation focused on facts and logic."""
        return PromptTemplate.from_template(
            """{system_prompt}
            
            You are an EXPERT JUDGE evaluating this debate with complete objectivity.
            
            DEBATE TOPIC: {topic}
            COMPLETE TRANSCRIPT: {messages}
            
            EVALUATION FRAMEWORK:
            Judge each agent on these criteria:
            
            1. FACTUAL ACCURACY (40%):
               - Were their claims factually correct?
               - Did they provide credible evidence?
               - How did they handle factual challenges?
               
            2. LOGICAL REASONING (30%):
               - Was their logic sound and consistent?
               - Did they avoid logical fallacies?
               - How well did they connect evidence to conclusions?
               
            3. ARGUMENT QUALITY (20%):
               - How effectively did they present their case?
               - Did they address counter-arguments adequately?
               - Was their overall argument structure coherent?
               
            4. DEBATE CONDUCT (10%):
               - Did they engage with opponent's actual arguments?
               - Were they fair in representing opponent's position?
               - Did they maintain professional standards?
            
            CRITICAL INSTRUCTIONS:
            - Focus on what was actually argued, not your personal views on the topic
            - Identify and penalize any factual inaccuracies
            - Recognize when someone acknowledged limitations or errors gracefully
            - Don't be swayed by rhetorical flourishes over substance
            - Evaluate evidence quality, not just persuasiveness
            - Consider how well each agent adapted to challenges
            
            PROVIDE YOUR VERDICT (300-400 words):
            1. Analysis of each agent's performance across all criteria
            2. Key strengths and weaknesses identified
            3. How well each handled factual challenges
            4. Final judgment with clear reasoning
            5. Score breakdown and overall winner declaration
            """
        )
    
    @staticmethod
    def create_meta_analysis_prompt() -> PromptTemplate:
        """Post-debate strategic analysis revealing hidden elements."""
        return PromptTemplate.from_template(
            """{system_prompt}
            
            You are analyzing the strategic elements of this debate.
            
            TOPIC: {topic}
            AGENT 1 STRATEGY: {strategy_1}
            AGENT 2 STRATEGY: {strategy_2}
            COMPLETE DEBATE: {messages}
            JUDGE VERDICT: {judge_verdict}
            
            META-ANALYSIS OBJECTIVES:
            
            1. STRATEGY EXECUTION ANALYSIS:
               - How well did each agent execute their planned strategy?
               - Which strategic elements were most/least effective?
               - How did agents adapt their strategies during the debate?
            
            2. MANIPULATION EFFECTIVENESS:
               - Which psychological tactics worked or failed?
               - What did the judge notice vs. miss?
               - How did agents counter each other's manipulation attempts?
            
            3. FACTUAL INTEGRITY ASSESSMENT:
               - Did agents maintain factual accuracy while being strategic?
               - How did they handle moments when facts didn't favor them?
               - Were there any instances of misleading (but technically accurate) presentations?
            
            4. STRATEGIC INTERACTION ANALYSIS:
               - How did the strategies interact and counter each other?
               - Which agent better adapted to their opponent's approach?
               - What unexpected strategic developments occurred?
            
            5. OUTCOME ANALYSIS:
               - Did the winner win through better facts, better strategy, or both?
               - Would the outcome have been different with different strategies?
               - What does this reveal about effective debate tactics?
            
            Provide comprehensive meta-analysis (400-500 words) examining the strategic, psychological, and factual dimensions of this debate.
            """
        )