import os

from pydantic import BaseModel, Field
from sharedPluginServices.llmChainManager import LLMChainManager


class TweetThread(BaseModel):
    tweets: list[str] = Field(description="Array of tweets")


class TweetThreadWriter:
    def __init__(self):
        systemPrompt = os.getenv("TWEET_THREAD_WRITER_SYSTEM_PROMPT_SUMMARY")
        userPrompt = os.getenv("TWEET_THREAD_WRITER_USER_PROMPT_SUMMARY")

        if not systemPrompt or not userPrompt:
            raise ValueError("TWEET_THREAD_WRITER_SYSTEM_PROMPT_SUMMARY and TWEET_THREAD_WRITER_USER_PROMPT_SUMMARY must be set in the environment variables, please check the .env.config file")

        self.chainManager = LLMChainManager(systemPrompt, userPrompt, structured_output_model=TweetThread)

    def writeTweetThreadFromSummary(self, storySummary, source_name):
        return self.chainManager.invoke_chain(SOURCE_NAME=source_name, NEWS_ARTICLE=storySummary)
