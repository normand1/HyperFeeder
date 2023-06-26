import json
import os
import tiktoken

from podcastSummaryPlugins.baseSummaryPlugin import BaseSummaryPlugin
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate


class StorySummaryPlugin(BaseSummaryPlugin):

    def identify(self) -> str:
        return "OpenAI Summarizer"

    def summarizeText(self, story):
        print("Summarizing text...")
        url = story["link"]
        print("Summarizing: " + url)
        texts = self.prepareForSummarization(story['rawSplitText'])
        summaryText = self.summarize(texts)
        return summaryText

    def prepareForSummarization(self, texts):

        if (self.num_tokens_from_string(texts) < (4096 - int(os.getenv('OPENAI_MAX_TOKENS_SUMMARY'))) - 265):
            return [texts]

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

    def summarize(self, texts):
        prompt_template = """Write a detailed summary of the following:
            {text}
            DETAILED SUMMARY:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        MAX_SUMMARY_SEGMENTS = int(os.getenv('MAX_SUMMARY_SEGMENTS'))
        docs = [Document(page_content=text) for text in texts[:MAX_SUMMARY_SEGMENTS]]
        llm = OpenAI(model=os.getenv('OPENAI_MODEL_SUMMARY'), max_tokens=int(os.getenv('OPENAI_MAX_TOKENS_SUMMARY')), temperature=0.2)
        chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=PROMPT, combine_prompt=PROMPT)
        result = chain.run(docs)
        return result
    
    def num_tokens_from_string(self, string: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(string))
        return num_tokens

plugin = StorySummaryPlugin()