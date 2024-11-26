import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain


class PodcastIntroWriter:
    def writeIntro(self, allStoryTitles, podcastName, typeOfPodcast):
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_SUMMARY"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS_SUMMARY")),
            temperature=0.3,
        )
        templateString = os.getenv("INTRO_TEMPLATE_STRING")
        prompt = PromptTemplate(
            input_variables=["allStoryTitles", "podcastName", "typeOfPodcast"],
            template=templateString,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.invoke(
            {
                "allStoryTitles": allStoryTitles,
                "podcastName": podcastName,
                "typeOfPodcast": typeOfPodcast,
            }
        )
