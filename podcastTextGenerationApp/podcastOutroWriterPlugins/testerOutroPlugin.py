from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin


class TesterOutroPlugin(BaseOutroWriterPlugin):
    def identify(self) -> str:
        return "🔬 tester outro plugin"

    def writeOutro(self, segments, introText):
        return "test outro text"


plugin = TesterOutroPlugin()
