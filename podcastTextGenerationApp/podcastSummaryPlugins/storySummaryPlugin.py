import os
from podcastSummaryPlugins.baseSummaryPlugin import BaseSummaryPlugin
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain


class StorySummaryPlugin(BaseSummaryPlugin):
    def identify(self) -> str:
        return "OpenAI Summarizer"

    def summarizeText(self, story):
        url = story["link"]
        print("Summarizing: " + url)
        texts = self.prepareForSummarization(story["rawSplitText"])
        summaryText = self.summarize(texts)
        return summaryText

    def summarize(self, texts):
        prompt_template = """Write a detailed summary of the following:
            {text}
            DETAILED SUMMARY:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        MAX_SUMMARY_SEGMENTS = int(os.getenv("MAX_SUMMARY_SEGMENTS"))
        docs = [Document(page_content=text) for text in texts[:MAX_SUMMARY_SEGMENTS]]

        # Initialize the OpenAI model
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_SUMMARY"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS_SUMMARY")),
            temperature=0.2,
        )

        # Load the summarization chain
        chain = load_summarize_chain(
            llm, chain_type="map_reduce", map_prompt=PROMPT, combine_prompt=PROMPT
        )

        # Run the chain and return the result
        result = chain.invoke(docs)
        return result["output_text"]


plugin = StorySummaryPlugin()
