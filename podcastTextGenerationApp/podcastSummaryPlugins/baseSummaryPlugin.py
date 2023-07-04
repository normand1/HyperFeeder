from abc import abstractmethod
import os, json, tiktoken
from podcastSummaryPlugins.abstractPluginDefinitions.abstractStorySummaryPlugin import AbstractStorySummaryPlugin
from langchain.text_splitter import CharacterTextSplitter

class BaseSummaryPlugin(AbstractStorySummaryPlugin):
    @abstractmethod
    def summarizeText(self, story):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    def writeToDisk(self, story, summaryText, summaryTextDirName, summaryTextFileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = summaryTextFileNameLambda(uniqueId, url)
        filePath = os.path.join(summaryTextDirName, rawTextFileName)
        os.makedirs(summaryTextDirName, exist_ok=True)
        with open(filePath, 'w') as file:
            json.dump(summaryText, file)
            file.flush()
    def doesOutputFileExist(self, story, summaryTextDirName, summaryTextFileNameLambda) -> bool:
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = summaryTextFileNameLambda(uniqueId, url)
        filePath = os.path.join(summaryTextDirName, rawTextFileName)
        if os.path.exists(filePath):
            print("Summary text file already exists at filepath: " + filePath + ", skipping summarizing story")
            return True
        else:
            return False
    def prepareForSummarization(self, texts):

        if (self.num_tokens_from_string(texts) < (4096 - int(os.getenv('OPENAI_MAX_TOKENS_SUMMARY'))) - 265):
            return [texts]

        CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator='.\n',
            chunk_size=CHUNK_SIZE,
            chunk_overlap=0 # no overlap
        )
        splitTexts = text_splitter.split_text(texts)
        if len(splitTexts) <= 2:
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator='<p>',
            chunk_size=CHUNK_SIZE,
            chunk_overlap=0 # no overlap
        )
            splitTexts = text_splitter.split_text(texts)
        if len(splitTexts) <= 2:
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator=' ',
            chunk_size=CHUNK_SIZE,
            chunk_overlap=0 # no overlap
        )
            splitTexts = text_splitter.split_text(texts)
        if len(splitTexts) <= 2:
            raise ValueError("Text cannot be summarized, please check the text and the above separators and try again.")
        return splitTexts
    def num_tokens_from_string(self, string: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(string))
        return num_tokens