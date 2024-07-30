import os
import re
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from anthropic import Anthropic


class StorySegmentWriter:
    def __init__(self, model_type="openai"):
        self.model_type = model_type

        if model_type == "openai":
            self.model = ChatOpenAI(
                model=os.getenv("OPENAI_MODEL_SUMMARY"),
                max_tokens=8096,
                temperature=float(os.getenv("OPENAI_TEMPERATURE_SUMMARY", "0.3")),
            )
        elif model_type == "claude":
            self.anthropic_client = Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                default_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"},
            )
        else:
            raise ValueError("Invalid model_type. Choose 'openai' or 'claude'.")

        self.parser = StrOutputParser()

        # Update the system prompt and user prompt
        self.system_prompt = "You are tasked with creating a podcast segment that discusses a news article in detail. Your goal is to present the information in an engaging and insightful manner, suitable for a podcast audience."
        self.user_prompt = """Follow these instructions carefully:

1. Begin by introducing the segment and mentioning the source of the news article:

<intro>
Next, we'll be examining an article titled {SOURCE_NAME}.
</intro>

2. The news article you will be discussing is as follows:

<article>
{NEWS_ARTICLE}
</article>

3. This segment should flow into and out of other segments easily and this segment should be modular and easy to swap with other segments, so no need to greet the audience. Include relevant information included beyond just the summary

4. Discuss the contents of the article in detail. Use transitions between topics to maintain a smooth flow.

5. As you discuss the article, make insightful comments about the content. Consider the following aspects:
   - The potential implications of the news
   - How it relates to broader trends or issues
   - Any unique or surprising elements in the story
   - Questions that the article raises but doesn't answer

6. Use a conversational tone appropriate for a podcast, but remain professional and informative.

Present your podcast segment within <podcast_segment> tags. Aim for a length that would take about 4-5 minutes to read aloud.

Remember to speak as if you're addressing a listening audience, not reading an essay. Use phrases like "As we can see from this article..." or "This brings up an interesting point..." to maintain an engaging, conversational style."""

        # Update the chain for OpenAI
        if model_type == "openai":
            self.prompt_template = ChatPromptTemplate.from_messages(
                [
                    ("system", self.system_prompt),
                    ("user", self.user_prompt),
                ]
            )
            self.chain = self.prompt_template | self.model | self.parser

    def writeSegmentFromSummary(self, storySummary, source_name):
        if self.model_type == "openai":
            # Create the input dictionary for the chain
            input_dict = {"SOURCE_NAME": source_name, "NEWS_ARTICLE": storySummary}
            # Run the chain and return the result
            return self.chain.invoke(input_dict)
        elif self.model_type == "claude":
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620",  # "claude-3-haiku-20240307"
                max_tokens=8096,  # 3000
                temperature=0.1,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.user_prompt.format(
                                    SOURCE_NAME=source_name, NEWS_ARTICLE=storySummary
                                ),
                            }
                        ],
                    }
                ],
            )
            # Remove HTML/XML tags from the response
            cleaned_text = re.sub(r"<[^>]+>", "", response.content[0].text)
            return cleaned_text
