import os
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain


class StorySummarizer:
    def __init__(self):
        # Ensure environment variables are set, with defaults
        model_name = os.getenv(
            "OPENAI_MODEL_SUMMARY", "gpt-3.5-turbo"
        )  # Default model name if not set
        max_tokens_summary = int(os.getenv("OPENAI_MAX_TOKENS_SUMMARY", "256"))
        self.llm = ChatOpenAI(
            model=model_name,
            max_tokens=max_tokens_summary,
            temperature=0,
        )

    def summarize(self, text):
        docs = [Document(page_content=text)]

        # Load the summarization chain
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")

        # Run the chain and return the result
        result = chain.run(docs)
        return result
