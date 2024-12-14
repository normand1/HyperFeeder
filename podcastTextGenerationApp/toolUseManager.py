from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from sharedPluginServices.llm_utils import initialize_llm_model
import hashlib


class ToolUseManager:
    def __init__(self):
        self.llmWithTools = None
        self.queryUniqueId = None
        self.query = None

    def initializeLLMWithTools(self, plugins: list[BaseDataSourcePlugin], excludedPlugins: list[str] = None):
        allTools = []
        for plugin in plugins:
            if excludedPlugins is None or plugin.plugin.identify(simpleName=True) not in excludedPlugins:
                allTools.extend(plugin.plugin.getTools())
        llm = initialize_llm_model()
        self.llmWithTools = llm.bind_tools(allTools)
        return self

    @staticmethod
    def toolUseManagerForSegmentResearch(initialQuery: str, plugins: dict, previousSegmentText: str = "", previousToolsUsed: list[str] = [], toolUseManagerCls=None):
        if not toolUseManagerCls:
            toolUseManagerCls = ToolUseManager
        researchQuery = (
            f"Based on previous findings:\n{previousSegmentText}\nNow please use tools to look deeper into: ```{initialQuery}```"
            if previousSegmentText.strip()
            else f"please use tools to look deep into this question: ```{initialQuery}```"
        )
        toolUseManager = toolUseManagerCls().initializeLLMWithTools(list(plugins.values()), excludedPlugins=previousToolsUsed)
        toolUseManager.query = researchQuery
        toolUseManager.queryUniqueId = hashlib.md5(researchQuery.encode()).hexdigest()
        return toolUseManager

    def invokeWithBoundToolsAndQuery(self):
        return self.llmWithTools.invoke(self.query)
