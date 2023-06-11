import json
import os

from podcastSummaryPlugins.abstractPluginDefinitions.abstractStorySummaryPlugin import AbstractStorySummaryPlugin
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

class storySummaryPlugin(AbstractStorySummaryPlugin):

    def identify(self) -> str:
        return "OpenAI Summarizer"

    def summarizeText(self, topStories, summaryTextDirNameLambda, summaryTextFileNameLambda):
        print("Summarizing text...")
        for story in topStories:
            url = story["link"]
            print("Summarizing: " + url)
            filePath = os.path.join(summaryTextDirNameLambda, summaryTextFileNameLambda(story["newsRank"], url))
            self.writeAndUpdateStorySummary(summaryTextDirNameLambda, filePath, story)

    def writeAndUpdateStorySummary(self, summaryTextDirNameLambda, summaryTextFileName, story):
        if not os.path.isfile(summaryTextFileName):
            directory = os.path.dirname(summaryTextDirNameLambda)
            os.makedirs(directory, exist_ok=True)  # Create the necessary directories
            with open(summaryTextFileName, 'w') as file:
                summaryText = self.summarize(" ".join(story["rawSplitText"][:2])) # Summarize the first two token splits of the story
                file.write(summaryText + "\n")
                file.flush()
        else:
            print("Skipping writing summary because it already exists")

    def summarize(self, text):
        docs = [Document(page_content=text)]
        llm = OpenAI(temperature=0)
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        result = chain.run(docs)
        return result

plugin = storySummaryPlugin()