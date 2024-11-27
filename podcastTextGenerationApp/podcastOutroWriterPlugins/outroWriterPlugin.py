import os
from langchain_openai import ChatOpenAI
from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, SystemMessage


class OutroWriterPlugin(BaseOutroWriterPlugin):
    def identify(self) -> str:
        return "🎸 outro writer plugin"

    def __init__(self):
        super().__init__()  # Call the __init__ method from the base class
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
        self.promptTemplate = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "The following text is the *intro* to my podcast. Write a funny joke I can make at the *outro* of the podcast based on this intro:\n\n```\n{introText}\n```\nAfter saying the joke make sure to end with an outro and invite the listener to tune in again soon.",
                ),
                ("user", "{introText}"),
            ]
        )

    def writeOutro(self, stories, introText):
        print("Writing funny Outro")
        # Create the input dictionary for the chain
        input_dict = {"introText": introText}

        # Generate the prompt
        prompt = self.promptTemplate.format_prompt(**input_dict).to_messages()

        # Ensure prompt is a list of BaseMessages
        if isinstance(prompt, BaseMessage):
            prompt = [prompt]
        elif not isinstance(prompt, list) or not all(isinstance(msg, BaseMessage) for msg in prompt):
            # Raise an error if the prompt is not properly formatted
            raise TypeError("Prompt must be a list of BaseMessages")

        # Pass the prompt to the model
        response = self.model.invoke(prompt)

        return self.parser.parse(response).content


plugin = OutroWriterPlugin()
