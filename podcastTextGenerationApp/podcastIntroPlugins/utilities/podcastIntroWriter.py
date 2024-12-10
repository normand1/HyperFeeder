import os
from sharedPluginServices.llmChainManager import LLMChainManager


class PodcastIntroWriter:
    def __init__(self):
        system_prompt = "You're a {typeOfPodcast} podcaster with a subtle wry sense of humor. Write a very short intro for a podcast covering these segments. Don't spend more than a sentence on each story. The podcast's name is {podcastName}. Do not include any introduction to the outro or any sound effects, simply provide the outro text directly without any additional chatter."
        user_prompt = "{allStoryTitles}"

        self.chain_manager = LLMChainManager(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=int(os.getenv("MAX_TOKENS_SUMMARY")),
        )

    def writeIntro(self, allStoryTitles, podcastName, typeOfPodcast):
        return self.chain_manager.invoke_chain(allStoryTitles=allStoryTitles, podcastName=podcastName, typeOfPodcast=typeOfPodcast)
