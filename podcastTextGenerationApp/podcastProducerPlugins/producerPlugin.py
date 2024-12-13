from podcastProducerPlugins.BaseProducerPlugin import BaseProducerPlugin


class ProducerPlugin(BaseProducerPlugin):
    def identify(self) -> str:
        return "💿 Producer plugin"

    def updateFileNames(
        self,
        segments,
        outroTextDirName,
        introDirName,
        segmentTextDirNameLambda,
        fileNameLambda,
    ):
        # update all of the filenames with an integer based on their ordering
        # The intro should be first
        self.renameFile(introDirName, "intro.txt", "0_intro.txt")

        # The segments should be next and ordered based on their rank
        for story in segments:
            uniqueId = story.uniqueId
            rank = story.newsRank
            filename = fileNameLambda(uniqueId)
            self.renameFile(segmentTextDirNameLambda, filename, f"{rank+1}_{filename}")

        self.renameFile(outroTextDirName, "outro.txt", f"{len(segments)+2}_outro.txt")


plugin = ProducerPlugin()
