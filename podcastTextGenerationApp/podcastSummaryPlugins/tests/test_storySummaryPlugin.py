import unittest
import os
from podcastSummaryPlugins import storySummaryPlugin

class TestsSorySummaryPlugin(unittest.TestCase):

    def test_identify(self):
        plugin = storySummaryPlugin.StorySummaryPlugin()
        self.assertEqual(plugin.identify(), 'OpenAI Summarizer')
    
    def test_prepareForSummarization_transcript_podnews(self):
        plugin = storySummaryPlugin.StorySummaryPlugin()
        os.environ["CHUNK_SIZE"] = "1000"
        texts = self.loadTranscript('podnews_transcript.txt')
        splitTexts = plugin.prepareForSummarization(texts)
        self.assertGreater(len(splitTexts), 10)
    
    def test_prepareForSummarization_transcript_podcasting_two(self):
        plugin = storySummaryPlugin.StorySummaryPlugin()
        os.environ["CHUNK_SIZE"] = "1000"
        texts = self.loadTranscript('podcastingTwoPointO_transcript.txt')
        splitTexts = plugin.prepareForSummarization(texts)
        self.assertGreater(len(splitTexts), 10)
    
    def test_prepareForSummarization_transcript_buzzcast(self):
        plugin = storySummaryPlugin.StorySummaryPlugin()
        os.environ["CHUNK_SIZE"] = "1000"
        texts = self.loadTranscript('buzzCast_transcript.txt')
        splitTexts = plugin.prepareForSummarization(texts)
        self.assertGreater(len(splitTexts), 10)
    
    def test_prepareForSummarization_article(self):
        plugin = storySummaryPlugin.StorySummaryPlugin()
        os.environ["CHUNK_SIZE"] = "1000"
        texts = self.loadTranscript('articleSummary.txt')
        splitTexts = plugin.prepareForSummarization(texts)
        self.assertGreater(len(splitTexts), 10)

    def test_prepareForSummarization_codeBlog(self):
        plugin = storySummaryPlugin.StorySummaryPlugin()
        os.environ["CHUNK_SIZE"] = "1000"
        texts = self.loadTranscript('blogWithCode.txt')
        splitTexts = plugin.prepareForSummarization(texts)
        [print(len(x)) for x in splitTexts]
        self.assertGreater(len(splitTexts), 10)
  
    def loadTranscript(self, transcriptName):
        current_directory = os.getcwd() + "/podcastTextGenerationApp/podcastSummaryPlugins/tests"
        file_path = f'{current_directory}/{transcriptName}'
        file = open(file_path, "r")
        file_contents = file.read()
        file.close()
        return file_contents

if __name__ == '__main__':
    unittest.main()