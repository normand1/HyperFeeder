from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import json


@dataclass
class SerializableMockResponse:
    tool_calls: List[Dict[str, Any]]
    content: str = "This is a mock response"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __json__(self):
        return self.to_dict()

    def __str__(self):
        return self.content


class SerializableMockEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SerializableMockResponse):
            return obj.to_dict()
        return super().default(obj)


class ToolUseResearchAgent:
    initializeLLMWithTools_calls = []
    invokeWithBoundToolsAndQuery_calls = []
    toolUseAgentForSecondaryResearch_calls = []
    toolUseAgentForSegmentResearch_calls = []
    handleFollowUpQuestionWithResearch_calls = []

    def __init__(self):
        self.llmWithTools = None
        self.queryUniqueId = None
        self.query = None

    def initializeLLMWithTools(self, plugins, excludedPlugins=None):
        ToolUseResearchAgent.initializeLLMWithTools_calls.append((plugins, excludedPlugins))
        return self

    def toolUseAgentForSegmentResearch(self):
        ToolUseResearchAgent.invokeWithBoundToolsAndQuery_calls.append(self.query)
        mock_response = SerializableMockResponse(tool_calls=[{"name": "TesterDataSourcePlugin-_-fetchStories", "args": {"searchQuery": f"research {self.query}"}}])
        return mock_response

    def handleFollowUpQuestionWithResearch(self, followUpQuery, followUpQuestionSegment):
        ToolUseResearchAgent.handleFollowUpQuestionWithResearch_calls.append((followUpQuery, followUpQuestionSegment))
        return f"Mock research answer for: {followUpQuery}"

    def invokeWithBoundToolsAndQuery(self):
        ToolUseResearchAgent.invokeWithBoundToolsAndQuery_calls.append(self.query)
        mock_response = SerializableMockResponse(tool_calls=[{"name": "TesterDataSourcePlugin-_-fetchStories", "args": {"searchQuery": f"research {self.query}"}}])
        return mock_response
