from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain


class PodcastIntroWriter:
    def writeIntro(self, allStoryTitles):
        llm = OpenAI(temperature=0.3)
        templateString = """You're a tech podcaster with a subtle wry sense of humor. Write a very short intro for a podcast covering these stories. Don't spend more than a sentence on each story. The podcasts name is "Autonomous Tech Podcast":
                        ```
                        {allStoryTitles}
                        ```
                        """
        prompt = PromptTemplate(
            input_variables=["allStoryTitles"],
            template=templateString,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(allStoryTitles)
