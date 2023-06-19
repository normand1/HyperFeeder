import json
import os
import tiktoken

from podcastSummaryPlugins.abstractPluginDefinitions.abstractStorySummaryPlugin import AbstractStorySummaryPlugin
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate


class StorySummaryPlugin(AbstractStorySummaryPlugin):

    def identify(self) -> str:
        return "OpenAI Summarizer"

    def summarizeText(self, topStories, summaryTextDirName, summaryTextFileNameLambda):
        print("Summarizing text...")
        for story in topStories:
            url = story["link"]
            print("Summarizing: " + url)
            filePath = os.path.join(summaryTextDirName, summaryTextFileNameLambda(story["newsRank"], url))
            texts = self.prepareForSummarization(story['rawSplitText'])
            self.writeAndUpdateStorySummary(summaryTextDirName, filePath, texts)

    def prepareForSummarization(self, texts):

        if (self.num_tokens_from_string(texts) < (4096 - 256)):
            return texts

        CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator='.\n',
            chunk_size=CHUNK_SIZE,
            chunk_overlap=0 # no overlap
        )
        splitTexts = text_splitter.split_text(texts)
        if len(splitTexts) <= 2:
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator='<p>',
            chunk_size=CHUNK_SIZE,
            chunk_overlap=0 # no overlap
        )
            splitTexts = text_splitter.split_text(texts)
        if len(splitTexts) <= 2:
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator=' ',
            chunk_size=CHUNK_SIZE,
            chunk_overlap=0 # no overlap
        )
            splitTexts = text_splitter.split_text(texts)
        if len(splitTexts) <= 2:
            raise ValueError("Text cannot be summarized, please check the text and the above separators and try again.")
        return splitTexts
    
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
        llm = OpenAI(model=os.getenv('OPENAI_MODEL_SUMMARY'), max_tokens=int(os.getenv('OPENAI_MAX_TOKENS_SUMMARY')), temperature=0.3)
        chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=PROMPT, combine_prompt=PROMPT)
        result = chain.run(docs)
        return result
    
    def num_tokens_from_string(self, string: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(string))
        return num_tokens

plugin = StorySummaryPlugin()