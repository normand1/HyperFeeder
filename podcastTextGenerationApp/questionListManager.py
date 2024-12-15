import hashlib
from pydantic import BaseModel, Field
from sharedPluginServices.llm_utils import initialize_llm_model
from colorama import Fore, Style


class Questions(BaseModel):
    questions: list[str] = Field(..., description="A list of interesting questions about the text.")


class QuestionsAgent:
    def __init__(self):
        self.llm = None
        self.queryUniqueId = None
        self.query = None

    def initializeLLM(self):
        self.llm = initialize_llm_model()
        return self

    @staticmethod
    def makeQuestionsAgent(text: str, questionListManagerCls=None):
        if not questionListManagerCls:
            questionListManagerCls = QuestionsAgent

        prompt = f"""
            Given the following text:

            {text}

            Please return a list of the most interesting questions one might ask about this text.
            Be sure to include enough context about the question for a standalong search about the question.
            """.strip()

        manager = questionListManagerCls().initializeLLM()
        manager.query = prompt
        manager.queryUniqueId = hashlib.md5(prompt.encode()).hexdigest()
        return manager

    def invoke(self):
        structuredLLM = self.llm.with_structured_output(Questions)
        response: Questions = structuredLLM.invoke(self.query)
        print(f"{Fore.GREEN}{Style.BRIGHT}Follow-up questions:{Style.RESET_ALL}")
        for question in response.questions:
            print(f"{Fore.CYAN}{question}{Style.RESET_ALL}")
        return response.questions
