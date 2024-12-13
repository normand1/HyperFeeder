import os
from sharedPluginServices.llmChainManager import LLMChainManager


class PodcastIntroWriter:
    def __init__(self):
        system_prompt = os.getenv("INTRO_WRITER_SYSTEM_PROMPT")
        user_prompt = os.getenv("INTRO_WRITER_USER_PROMPT")

        self.chain_manager = LLMChainManager(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=int(os.getenv("MAX_TOKENS_SUMMARY")),
        )

    def writeIntro(self, combinedStorySegments, podcastName, typeOfPodcast):
        return self.chain_manager.invoke_chain(combinedStorySegments=combinedStorySegments, podcastName=podcastName, typeOfPodcast=typeOfPodcast)
