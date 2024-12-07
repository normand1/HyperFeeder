import os
from sharedPluginServices.llmChainManager import LLMChainManager
from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin
from dotenv import load_dotenv


class OutroWriterPlugin(BaseOutroWriterPlugin):
    def identify(self) -> str:
        return "🎸 outro writer plugin"

    def __init__(self):
        super().__init__()  # Call the __init__ method from the base class
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.outro"))

        system_prompt = "The following text is the *intro* to my podcast. Write a funny joke I can make at the *outro* of the podcast based on this intro:\n\n```\n{introText}\n```\nAfter saying the joke make sure to end with an outro and invite the listener to tune in again soon."
        user_prompt = "{introText}"

        self.chain_manager = LLMChainManager(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS_OUTRO")),
        )

    def writeOutro(self, stories, introText):
        print("Writing funny Outro")
        return self.chain_manager.invoke_chain(introText=introText)


plugin = OutroWriterPlugin()
