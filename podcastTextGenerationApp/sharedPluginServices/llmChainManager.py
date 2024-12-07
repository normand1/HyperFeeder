import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class LLMChainManager:
    def __init__(
        self,
        system_prompt=None,
        user_prompt=None,
        system_prompt_env_var=None,
        user_prompt_file_env_var=None,
        model_version_env_var="LLM_MODEL_VERSION_NAME",
        max_tokens=8096,
    ):
        self.model_type = os.getenv("LLM_MODEL_PROVIDER")

        # Handle prompts
        self.system_prompt = system_prompt or os.getenv(system_prompt_env_var)
        if user_prompt_file_env_var:
            with open(os.getenv(user_prompt_file_env_var), "r", encoding="utf-8") as file:
                self.user_prompt = file.read()
        else:
            self.user_prompt = user_prompt

        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", self.user_prompt),
            ]
        )
        self.parser = StrOutputParser()

        # Initialize the appropriate model
        if self.model_type == "openai":
            model = ChatOpenAI(model=os.getenv(model_version_env_var), max_tokens=max_tokens, temperature=float(os.getenv("OPENAI_TEMPERATURE_SUMMARY")))
        elif self.model_type == "anthropic":
            model = ChatAnthropic(model=os.getenv(model_version_env_var), max_tokens=max_tokens, temperature=float(os.getenv("OPENAI_TEMPERATURE_SUMMARY")))
        else:
            raise ValueError("Invalid model_type. Choose 'openai' or 'anthropic'.")

        # Create the chain
        self.chain = self.prompt_template | model | self.parser

    def invoke_chain(self, **kwargs):
        """
        Invoke the LLM chain with the given keyword arguments
        """
        return self.chain.invoke(kwargs)
