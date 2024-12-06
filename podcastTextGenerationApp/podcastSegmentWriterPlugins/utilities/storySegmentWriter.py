import os, re
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


class StorySegmentWriter:
    def __init__(self, model_type="openai"):
        self.model_type = model_type
        self.system_prompt = os.getenv("SYSTEM_PROMPT_SUMMARY")

        with open(os.getenv("USER_PROMPT_SUMMARY"), "r", encoding="utf-8") as file:
            self.user_prompt = file.read()

        if model_type == "openai":
            self.model = ChatOpenAI(model=os.getenv("OPENAI_MODEL_SUMMARY"), max_tokens=8096, temperature=float(os.getenv("OPENAI_TEMPERATURE_SUMMARY", "0.3")))
            self.parser = StrOutputParser()
            self.prompt_template = ChatPromptTemplate.from_messages(
                [
                    ("system", self.system_prompt),
                    ("user", self.user_prompt),
                ]
            )
            self.chain = self.prompt_template | self.model | self.parser
        elif model_type == "anthropic":
            self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            raise ValueError("Invalid model_type. Choose 'openai' or 'anthropic'.")

    def writeSegmentFromSummary(self, storySummary, source_name):
        if self.model_type == "openai":
            return self.chain.invoke({"SOURCE_NAME": source_name, "NEWS_ARTICLE": storySummary})
        prompt = f"{HUMAN_PROMPT} {self.user_prompt.format(SOURCE_NAME=source_name,NEWS_ARTICLE=storySummary)}{AI_PROMPT}"
        resp = self.anthropic_client.completions.create(model="claude-3-5-sonnet-latest", max_tokens_to_sample=8096, temperature=0.1, prompt=f"{self.system_prompt}\n\n{prompt}")
        return re.sub(r"<[^>]+>", "", resp.completion)
