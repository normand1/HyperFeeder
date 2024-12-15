from pydantic import BaseModel, Field


class Questions(BaseModel):
    questions: list[str] = Field(..., description="A list of interesting questions about the text.")
    answers: list[str] = Field(..., description="A list of answers to the questions.")
    sources: list[str] = Field(..., description="A list of sources used to answer the questions.")


class MockQuestionsAgent:
    initializeLLM_calls = []
    invoke_calls = []

    def __init__(self):
        self.llm = None
        self.queryUniqueId = None
        self.query = None

    def initializeLLM(self):
        MockQuestionsAgent.initializeLLM_calls.append(True)
        return self

    @staticmethod
    def makeQuestionsAgent(text: str, questionListManagerCls=None):
        if not questionListManagerCls:
            questionListManagerCls = MockQuestionsAgent

        prompt = f"""
            Given the following text:

            {text}

            Please return a list of the most interesting questions one might ask about this text.
            Be sure to include enough context about the question for a standalong search about the question.
            """.strip()

        manager = questionListManagerCls().initializeLLM()
        manager.query = prompt
        manager.queryUniqueId = "mock_hash_id"
        return manager

    def invoke(self):
        MockQuestionsAgent.invoke_calls.append(self.query)
        mock_questions = ["Mock question 1 about the text?", "Mock question 2 about the text?", "Mock question 3 about the text?"]
        return mock_questions
