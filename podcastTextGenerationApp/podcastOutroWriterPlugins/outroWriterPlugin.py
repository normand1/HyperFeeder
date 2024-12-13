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

        system_prompt = os.getenv("OUTRO_WRITER_SYSTEM_PROMPT")
        user_prompt = os.getenv("OUTRO_WRITER_USER_PROMPT")

        self.chain_manager = LLMChainManager(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS_OUTRO")),
        )

    def writeOutro(self, segments, introText):
        print("Writing funny Outro")
        return self.chain_manager.invoke_chain(introText=introText)


plugin = OutroWriterPlugin()
