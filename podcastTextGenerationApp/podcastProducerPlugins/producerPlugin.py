from podcastProducerPlugins.BaseProducerPlugin import BaseProducerPlugin

class ProducerPlugin(BaseProducerPlugin):

    def identify(self) -> str:
        return "Producer plugin"
    
    def updateFileNames(self, stories, outroTextDirName, introDirName, segmentTextDirNameLambda, fileNameLambda):
        
        # update all of the filenames with an integer based on their ordering
        # The intro should be first
        self.rename_file(introDirName, "intro.txt", "0_intro.txt")

        # The segments should be next and ordered based on their rank
        for i, story in enumerate(stories):
            url = story["link"]
            uniqueId = story["uniqueId"]
            rank = story["newsRank"]
            filename = fileNameLambda(uniqueId, url)
            self.rename_file(segmentTextDirNameLambda, filename, f"{rank+1}_{filename}")

        self.rename_file(outroTextDirName, "outro.txt", f"{len(stories)+2}_outro.txt")

plugin = ProducerPlugin()