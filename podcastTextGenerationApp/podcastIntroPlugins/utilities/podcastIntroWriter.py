from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os


class PodcastIntroWriter:
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
                    "You're a {typeOfPodcast} podcaster with a subtle wry sense of humor. Write a very short intro for a podcast covering these stories. Don't spend more than a sentence on each story. The podcast's name is {podcastName}:",
                ),
                ("user", "{allStoryTitles}"),
            ]
        )

        # Combine the components into a chain
        self.chain = self.prompt_template | self.model | self.parser

    def writeIntro(self, allStoryTitles, podcastName, typeOfPodcast):
        # Create the input dictionary for the chain
        input_dict = {
            "allStoryTitles": allStoryTitles,
            "podcastName": podcastName,
            "typeOfPodcast": typeOfPodcast,
        }

        # Run the chain and return the result
        return self.chain.invoke(input_dict)
