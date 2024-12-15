from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.segment import Segment
from sharedPluginServices.llm_utils import initialize_llm_model
import hashlib


class ToolUseResearchAgent:
    def __init__(self):
        self.llmWithTools = None
        self.llmWithoutTools = None
        self.queryUniqueId = None
        self.query = None

    def initializeLLMWithTools(self, plugins: list[BaseDataSourcePlugin], excludedPlugins: list[str] = None):
        allTools = []
        for plugin in plugins:
            if excludedPlugins is None or plugin.plugin.identify(simpleName=True) not in excludedPlugins:
                allTools.extend(plugin.plugin.getTools())
        llm = initialize_llm_model()
        self.llmWithTools = llm.bind_tools(allTools)
        self.llmWithoutTools = initialize_llm_model()
        return self

    @staticmethod
    def toolUseAgentForSegmentResearch(initialQuery: str, plugins: dict, toolUseManagerCls=None):
        if not toolUseManagerCls:
            toolUseManagerCls = ToolUseResearchAgent
        researchQuery = f"please use tools to look deep into this question: ```{initialQuery}```"
        toolUseResearchAgent = toolUseManagerCls().initializeLLMWithTools(list(plugins.values()))
        toolUseResearchAgent.query = researchQuery
        toolUseResearchAgent.queryUniqueId = hashlib.md5(researchQuery.encode()).hexdigest()
        return toolUseResearchAgent

    @staticmethod
    def toolUseAgentForSecondaryResearch(initialQuery: str, plugins: dict, previousToolsUsed: list[str], toolUseManagerCls=None):
        if not toolUseManagerCls:
            toolUseManagerCls = ToolUseResearchAgent
        researchQuery = f"Use tools if needed, if tools are not needed simply return the answer. Please answer the following question: ```{initialQuery}```"
        toolUseResearchAgent = toolUseManagerCls().initializeLLMWithTools(list(plugins.values()), excludedPlugins=previousToolsUsed)
        toolUseResearchAgent.query = researchQuery
        toolUseResearchAgent.queryUniqueId = hashlib.md5(researchQuery.encode()).hexdigest()
        return toolUseResearchAgent

    def handleFollowUpQuestionWithResearch(self, followUpQuery: str, followUpQuestionSegment: Segment):
        refinedQuery = (
            f"Original question: {followUpQuery}\nTool results:\n{followUpQuestionSegment.joinAllSources(1)}\n\n"
            f"Please provide a more comprehensive and accurate final answer based on the above context."
        )
        refinedAnswerResponse = self.llmWithoutTools.invoke(refinedQuery)
        return refinedAnswerResponse.content

    def invokeWithBoundToolsAndQuery(self):
        return self.llmWithTools.invoke(self.query)
