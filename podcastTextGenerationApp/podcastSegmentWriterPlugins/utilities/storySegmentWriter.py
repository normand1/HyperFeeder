import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class StorySegmentWriter:
    def __init__(self):
        self.model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_SUMMARY"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS_SUMMARY")),
            temperature=0.3,
        )
        self.parser = StrOutputParser()

        # Define the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Relay this story to listeners in a segment for a podcast. Do not say welcome back or outro the segment, but please introduce the story quickly before poceeding with the segment, this segment should flow into and out of other segments easily and this segment should be modular and easy to swap with other segments. Include relevant information included beyond just the summary:\n\n```\n{storySummary}\n```\nPlease include only the host's dialogue in the answer without specifying the speaker and don't include intro or outro tags.",
                ),
                ("user", "{storySummary}"),
            ]
        )

        # Combine the components into a chain
        self.chain = self.prompt_template | self.model | self.parser

    def writeSegmentFromSummary(self, storySummary):
        # Create the input dictionary for the chain
        input_dict = {"storySummary": storySummary}

        # Run the chain and return the result
        return self.chain.invoke(input_dict)


# Example usage:
# writer = StorySegmentWriter()
# segment = writer.writeSegmentFromSummary("A quick summary of the story...")
# print(segment)
