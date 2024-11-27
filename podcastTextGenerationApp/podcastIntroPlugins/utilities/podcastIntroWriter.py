import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage


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

    def writeIntro(self, allStoryTitles, podcastName, typeOfPodcast):
        # Create the input dictionary for the chain
        input_dict = {
            "allStoryTitles": allStoryTitles,
            "podcastName": podcastName,
            "typeOfPodcast": typeOfPodcast,
        }

        # Generate the prompt
        prompt = self.prompt_template.format_prompt(**input_dict).to_messages()

        # Convert prompt to a list of BaseMessages if necessary
        if isinstance(prompt, BaseMessage):
            prompt = [prompt]
        elif not isinstance(prompt, list) or not all(isinstance(msg, BaseMessage) for msg in prompt):
            raise TypeError("Prompt must be a list of BaseMessages")

        # Pass the prompt to the model and parse the response

        response = self.model.invoke(prompt)

        return self.parser.parse(response)
