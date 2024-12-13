from sharedPluginServices.llmChainManager import LLMChainManager
import os


class StorySegmentWriter:
    def __init__(self):
        systemPrompt = os.getenv("STORY_WRITER_SYSTEM_PROMPT_SUMMARY")
        userPrompt = os.getenv("STORY_WRITER_USER_PROMPT_SUMMARY")

        if not systemPrompt or not userPrompt:
            raise ValueError("STORY_WRITER_SYSTEM_PROMPT_SUMMARY and STORY_WRITER_USER_PROMPT_SUMMARY must be set in the environment variables, please check the .env.config file")

        self.chainManager = LLMChainManager(systemPrompt, userPrompt)

    def writeSegmentFromSummary(self, storySummary, source_name):
        return self.chainManager.invoke_chain(SOURCE_NAME=source_name, NEWS_ARTICLE=storySummary)
