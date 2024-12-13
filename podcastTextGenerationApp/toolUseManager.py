from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from sharedPluginServices.llm_utils import initialize_llm_model
from podcastDataSourcePlugins.tavilyDataSourcePlugin import TavilyDataSourcePlugin
import hashlib


class ToolUseManager:

    def __init__(self):
        self.llmWithTools = None
        self.queryUniqueId = None
        self.query = None

    def initializeLLMWithTools(self, plugins: list[BaseDataSourcePlugin], excludedPlugins: list[str] = None):
        allTools = []
        for plugin in plugins:
            # Only include tools from specified plugins, or all if no restrictions
            if excludedPlugins is None or plugin.plugin.identify(simpleName=True) not in excludedPlugins:
                foundTools = plugin.plugin.getTools()
                allTools.extend(foundTools)

        llm = initialize_llm_model()
        llmWithTools = llm.bind_tools(allTools)
        self.llmWithTools = llmWithTools
        return self

    @staticmethod
    def toolUseManagerForSegmentResearch(initialQuery: str, plugins: list[BaseDataSourcePlugin], previousSegmentText: str = "", previousToolsUsed: list[str] = []):
        if previousSegmentText.strip():
            researchQuery = f"Based on previous findings:\n{previousSegmentText}\nNow please use tools to look deeper into: ```{initialQuery}```"
        else:
            researchQuery = f"please use tools to look deep into this question: ```{initialQuery}```"

        # Exclude previously used tools
        toolUseManager = (ToolUseManager()).initializeLLMWithTools(list(plugins.values()), excludedPlugins=previousToolsUsed)
        toolUseManager.query = researchQuery
        toolUseManager.queryUniqueId = hashlib.md5(researchQuery.encode()).hexdigest()
        return toolUseManager

    def invokeWithBoundToolsAndQuery(self):
        toolCallResponse = self.llmWithTools.invoke(self.query)
        return toolCallResponse
