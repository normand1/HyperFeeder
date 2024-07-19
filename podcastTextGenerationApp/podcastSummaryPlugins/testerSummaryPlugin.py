from podcastSummaryPlugins.baseSummaryPlugin import BaseSummaryPlugin


class TesterSummaryPlugin(BaseSummaryPlugin):
    def identify(self) -> str:
        return "🧪📓 tester summary plugin"

    def summarizeText(self, story):
        assert story is not None
        assert story["link"] is not None
        assert story["rawSplitText"] is not None
        texts = self.prepareForSummarization(story["rawSplitText"])
        summaryText = self.summarize(texts)
        return summaryText

    def summarize(self, texts):
        return "test summary text"


plugin = TesterSummaryPlugin()
