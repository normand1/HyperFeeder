import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin

class FunnyOutroWriterPlugin(BaseOutroWriterPlugin):

    def identify(self) -> str:
        return "😜 funny outro writer plugin"
    
    def writeOutro(self, stories, introText):
        
        print("Writing funny Outro")
        llm = OpenAI(model=os.getenv('OPENAI_MODEL_SUMMARY'), max_tokens=int(os.getenv('OPENAI_MAX_TOKENS_OUTRO')), temperature=0.3)
        templateString = """This is the intro to my podcast. Write a funny joke I can make at the outro of the podcast based on this intro:

                            ```
                            {introText}
                            ```
                            After saying the joke make sure to end with an outro and invite the listener to tune in again soon.
                        """
        prompt = PromptTemplate(
            input_variables=["introText"],
            template=templateString,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(introText)

plugin = FunnyOutroWriterPlugin()