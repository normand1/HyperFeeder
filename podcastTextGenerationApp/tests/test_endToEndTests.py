import unittest
import os
from podcastTextGenerationApp.app import App

class EndToEndTests(unittest.TestCase):

    def test_appRun(self):
        # Override Environment Variables For Testing
        os.environ['PODCAST_NAME'] = 'Test Podcast'
        os.environ['PODCAST_TYPE'] = 'Test Podcast Type'
        os.environ['PODCAST_DATA_SOURCE_PLUGINS']='testerDataSourcePlugin'
        os.environ['PODCAST_INTRO_PLUGINS']='testerIntroPlugin'
        os.environ['PODCAST_SCRAPER_PLUGINS']='testerScraperPlugin'
        os.environ['PODCAST_SUMMARY_PLUGINS']='testerSummaryPlugin'
        os.environ['PODCAST_SEGMENT_WRITER_PLUGINS']='testerSegmentWriter'
        os.environ['PODCAST_OUTRO_PLUGINS']='testerOutroPlugin'
        os.environ['PODCAST_PRODUCER_PLUGINS']='producerPlugin'

        # Clear Previous Test Artifacts
        if os.path.exists('output/test-podcast'):
            os.system('rm -rf output/test-podcast')
            
        # Run App
        App().run('test-podcast')