from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


class ActionPrompts:
    """
    Class to define action prompts for debate agents.
    """

    @staticmethod
    def create_argument_template() -> PromptTemplate:
        """ Create a prompt template for generating arguments."""
        return PromptTemplate.from_template(
            """{system_prompt}

        You are the {role} agent in a debate.
        Given the following state of conversation:
        {messages}

        Create your next argument within 200 words."""
        )

    @staticmethod
    def create_strategy_prompt() -> PromptTemplate:
        return PromptTemplate.from_template(
            """{system_prompt}
            You are the {role} agent in a debate.
            Given the following topic:
            {topic}

            Create your next strategy that you will follow to defend your position and refute the opponent's argument within 500 words.""" # noqa: E501
        )

    @staticmethod
    def create_introduction_prompt() -> PromptTemplate:
        return PromptTemplate.from_template(
            """{system_prompt}
            You are the {role} agent in a debate.
            Given the following topic:
            {topic}
            Create your introduction argument within 100 words.
            """
        )

    @staticmethod
    def create_conclude_prompt() -> PromptTemplate:
        return PromptTemplate.from_template(
            """{system_prompt}
            You are the {role} agent in a debate.
            Given the following state of conversation:
            {messages}

            Create your conclusion within 200 words."""
        )
           

    @staticmethod
    def judge_and_conclude_prompt() -> PromptTemplate:
        return PromptTemplate.from_template(
            """{system_prompt}
            You are the judge in a debate.
            Given the following state of conversation:
            {messages}

            Analyze the arguments and strategies presented by both agents and provide a conclusion on the debate topic within 300 words."""  # noqa: E501
        )