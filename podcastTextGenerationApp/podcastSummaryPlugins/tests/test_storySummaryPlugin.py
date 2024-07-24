import unittest
import os
from podcastSummaryPlugins import storySummaryPlugin


class TestsStorySummaryPlugin(unittest.TestCase):
    def test_identify(self):
        plugin = storySummaryPlugin.StorySummaryPlugin()
        self.assertEqual(plugin.identify(), "📓 OpenAI Summarizer")

    def loadTranscript(self, transcriptName):
        current_directory = (
            os.getcwd() + "/podcastTextGenerationApp/podcastSummaryPlugins/tests"
        )
        file_path = f"{current_directory}/{transcriptName}"
        file = open(file_path, "r")
        file_contents = file.read()
        file.close()
        return file_contents


if __name__ == "__main__":
    unittest.main()
