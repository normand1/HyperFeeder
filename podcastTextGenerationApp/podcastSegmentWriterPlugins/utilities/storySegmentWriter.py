import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain


class StorySegmentWriter:
    def writeSegmentFromSummary(self, storySummary):
        llm = OpenAI(
            model=os.getenv("OPENAI_MODEL_SUMMARY"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS_SUMMARY")),
            temperature=0.3,
        )
        templateString = """Relay this story to listeners in a short segment for a podcast. Do not say welcome back or outro the segment, this segment should flow into and out of other segments easily and this segment should be modular and easy to swap with other segments. Include relevant information included beyond just the summary
                            ```
                            {storySummary}
                            ```
                            Please include only the host's dialogue in the answer without specifying the speaker and don't include intro or outro tags.
                        """
        prompt = PromptTemplate(
            input_variables=["storySummary"],
            template=templateString,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(storySummary)
