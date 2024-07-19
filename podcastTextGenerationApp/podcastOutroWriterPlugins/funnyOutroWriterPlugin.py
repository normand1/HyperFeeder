import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin
from dotenv import load_dotenv


class FunnyOutroWriterPlugin(BaseOutroWriterPlugin):
    def identify(self) -> str:
        return "😜 funny outro writer plugin"

    def __init__(self):
        self.parser = StrOutputParser()
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.outro"))
        self.model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_SUMMARY"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS_OUTRO")),
            temperature=0.3,
        )

        # Define the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "The following text is the *intro* to my podcast. Write a funny joke I can make at the *outro* of the podcast based on this intro:\n\n```\n{introText}\n```\nAfter saying the joke make sure to end with an outro and invite the listener to tune in again soon.",
                ),
                ("user", "{introText}"),
            ]
        )

        # Combine the components into a chain
        self.chain = self.prompt_template | self.model | self.parser

    def writeOutro(self, stories, introText):
        print("Writing funny Outro")
        # Create the input dictionary for the chain
        input_dict = {"introText": introText}

        # Run the chain and return the result
        return self.chain.invoke(input_dict)


plugin = FunnyOutroWriterPlugin()
