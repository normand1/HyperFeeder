from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from sharedPluginServices.llm_utils import initialize_llm_model


class PublicationPlanningManager:
    def generatePublicationStructure(self, publicationRequestText: str, plugins: list[BaseDataSourcePlugin], allowed_plugin_names: list[str] = None):
        allTools = []
        for plugin in plugins:
            # Only include tools from specified plugins, or all if no restrictions
            if allowed_plugin_names is None or plugin.plugin.identify(simpleName=True) in allowed_plugin_names:
                print(f"Looking for tools from {plugin.plugin.identify(simpleName=True)}")
                foundTools = plugin.plugin.getTools()
                print(f"Found tools: {foundTools}")
                allTools.extend(foundTools)

        llm = initialize_llm_model()
        llmWithTools = llm.bind_tools(allTools)
        return llmWithTools.invoke(publicationRequestText)
