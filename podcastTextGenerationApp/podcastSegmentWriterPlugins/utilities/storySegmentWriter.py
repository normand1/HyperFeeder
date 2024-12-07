from sharedPluginServices.llmChainManager import LLMChainManager


class StorySegmentWriter:
    def __init__(self):
        self.chain_manager = LLMChainManager(system_prompt_env_var="SYSTEM_PROMPT_SUMMARY", user_prompt_file_env_var="USER_PROMPT_SUMMARY")

    def writeSegmentFromSummary(self, storySummary, source_name):
        return self.chain_manager.invoke_chain(SOURCE_NAME=source_name, NEWS_ARTICLE=storySummary)
