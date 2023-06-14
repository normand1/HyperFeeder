from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os

class PodcastIntroWriter:
    def writeIntro(self, allStoryTitles, podcastName, typeOfPodcast):
        llm = OpenAI(model=os.getenv('OPENAI_MODEL_SUMMARY'), max_tokens=int(os.getenv('OPENAI_MAX_TOKENS_SUMMARY')), temperature=0.3)
        templateString = """You're a {typeOfPodcast} podcaster with a subtle wry sense of humor. Write a very short intro for a podcast covering these stories. Don't spend more than a sentence on each story. The podcasts name is {podcastName}:
                        ```
                        {allStoryTitles}
                        ```
                        """
        prompt = PromptTemplate(
            input_variables=["allStoryTitles", "podcastName", "typeOfPodcast"],
            template=templateString,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run({'allStoryTitles': allStoryTitles, 'podcastName': podcastName, 'typeOfPodcast': typeOfPodcast})
