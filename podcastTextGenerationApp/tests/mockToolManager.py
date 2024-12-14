from unittest.mock import MagicMock


class MockToolUseManager:
    initializeLLMWithTools_calls = []
    invokeWithBoundToolsAndQuery_calls = []

    def __init__(self):
        self.llmWithTools = None
        self.queryUniqueId = None
        self.query = None

    def initializeLLMWithTools(self, plugins, excludedPlugins=None):
        MockToolUseManager.initializeLLMWithTools_calls.append((plugins, excludedPlugins))
        return self

    def invokeWithBoundToolsAndQuery(self):
        MockToolUseManager.invokeWithBoundToolsAndQuery_calls.append(self.query)
        mock_response = MagicMock()
        mock_response.tool_calls = [{"name": "TesterDataSourcePlugin-_-fetchStories", "args": {"searchQuery": f"research {self.query}"}}]
        return mock_response
