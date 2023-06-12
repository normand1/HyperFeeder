import json
import os

from podcastSummaryPlugins.abstractPluginDefinitions.abstractStorySummaryPlugin import AbstractStorySummaryPlugin
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate

class storySummaryPlugin(AbstractStorySummaryPlugin):

    def identify(self) -> str:
        return "OpenAI Summarizer"

    def summarizeText(self, topStories, summaryTextDirNameLambda, summaryTextFileNameLambda):
        print("Summarizing text...")
        for story in topStories:
            url = story["link"]
            print("Summarizing: " + url)
            filePath = os.path.join(summaryTextDirNameLambda, summaryTextFileNameLambda(story["newsRank"], url))
            texts = self.prepareForSummarization(story['rawSplitText'])
            self.writeAndUpdateStorySummary(summaryTextDirNameLambda, filePath, texts)

    def prepareForSummarization(self, texts):
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator='.\n',
            chunk_size=2000,
            chunk_overlap=0 # no overlap
        )
        texts = text_splitter.split_text(texts)
        return texts
    
    def writeAndUpdateStorySummary(self, summaryTextDirNameLambda, summaryTextFileName, texts):
        if not os.path.isfile(summaryTextFileName):
            directory = os.path.dirname(summaryTextDirNameLambda)
            os.makedirs(directory, exist_ok=True)  # Create the necessary directories
            with open(summaryTextFileName, 'w') as file:
                summaryText = self.summarize(texts)
                file.write(summaryText + "\n")
                file.flush()
        else:
            print("Skipping writing summary because it already exists")

    def summarize(self, texts):
        prompt_template = """Write a detailed summary of the following:
            {text}
            DETAILED SUMMARY:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        MAX_SUMMARY_SEGMENTS = int(os.getenv('MAX_SUMMARY_SEGMENTS'))
        docs = [Document(page_content=text) for text in texts[:MAX_SUMMARY_SEGMENTS]]
        llm = OpenAI(temperature=0)
        chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=PROMPT, combine_prompt=PROMPT)
        result = chain.run(docs)
        return result

plugin = storySummaryPlugin()