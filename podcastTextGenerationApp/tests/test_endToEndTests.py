import os
import unittest
from unittest.mock import MagicMock

from podcastTextGenerator import PodcastTextGenerator
from publicationPlanningManager import PublicationPlanningManager


class EndToEndTests(unittest.TestCase):
    def test_appRun(self):
        # Override Environment Variables For Testing
        os.environ["PODCAST_NAME"] = "Test Podcast"
        os.environ["PODCAST_TYPE"] = "Test Podcast Type"
        os.environ["PODCAST_DATA_SOURCE_PLUGINS"] = "testerDataSourcePlugin"
        os.environ["PODCAST_INTRO_PLUGINS"] = "testerIntroPlugin"
        os.environ["PODCAST_SCRAPER_PLUGINS"] = "testerScraperPlugin"
        os.environ["PODCAST_RESEARCHER_PLUGINS"] = "testResearcherPlugin"
        os.environ["PODCAST_SUMMARY_PLUGINS"] = "testerSummaryPlugin"
        os.environ["PODCAST_SEGMENT_WRITER_PLUGINS"] = "testerSegmentWriter"
        os.environ["PODCAST_OUTRO_PLUGINS"] = "testerOutroPlugin"
        os.environ["PODCAST_PRODUCER_PLUGINS"] = "producerPlugin"
        os.environ["SHOULD_PAUSE_AND_VALIDATE_STORIES_BEFORE_SCRAPING"] = "false"

        # Clear Previous Test Artifacts
        if os.path.exists("output/test-podcast"):
            os.system("rm -rf output/test-podcast")

        # Create mock planning managers
        mock_initial_planning_manager = MagicMock(spec=PublicationPlanningManager)
        mock_research_planning_manager = MagicMock(spec=PublicationPlanningManager)

        # Configure mock initial planning manager
        def mock_generate_structure(query, plugins, allowed_plugin_names: list[str] = ["testerDataSourcePlugin"]):
            mock_structure = MagicMock()
            mock_structure.tool_calls = [{"name": "TesterDataSourcePlugin-_-fetchStories", "args": {"searchQuery": query}}]
            return mock_structure

        mock_initial_planning_manager.generatePublicationStructure.side_effect = mock_generate_structure

        # Configure mock research planning manager
        def mock_research_structure(query, plugins):
            mock_structure = MagicMock()
            mock_structure.tool_calls = [{"name": "TesterDataSourcePlugin-_-fetchStories", "args": {"searchQuery": "research " + query}}]
            return mock_structure

        mock_research_planning_manager.generatePublicationStructure.side_effect = mock_research_structure

        # Run App with mock planning managers
        PodcastTextGenerator().run(
            "test-podcast",
            initialPlanningManager=mock_initial_planning_manager,
            researchPlanningManager=mock_research_planning_manager,
            additionalAllowedPluginNamesForInitialResearch=["testerDataSourcePlugin"],
        )

        # Verify planning managers were called
        mock_initial_planning_manager.generatePublicationStructure.assert_called()
        mock_research_planning_manager.generatePublicationStructure.assert_called()

        # Check if the correct files were added to the output directory
        output_dir = "output/test-podcast"
        expected_files = {
            "intro_text": ["0_intro.txt"],
            "segment_text": ["1_be937e905acfe59971566b5bbec93262.txt"],
            "outro_text": ["3_outro.txt"],
        }

        for subdir, files in expected_files.items():
            subdir_path = os.path.join(output_dir, subdir)
            self.assertTrue(
                os.path.exists(subdir_path),
                f"Directory {subdir} does not exist in {output_dir}",
            )

            for file in files:
                file_path = os.path.join(subdir_path, file)
                self.assertTrue(
                    os.path.exists(file_path),
                    f"File {file} does not exist in {subdir_path}",
                )

            # Check if there are no unexpected files in the subdirectory
            actual_files = os.listdir(subdir_path)
            self.assertEqual(
                len(actual_files),
                len(files),
                f"Unexpected number of files in {subdir_path}",
            )

            for file in actual_files:
                self.assertIn(file, files, f"Unexpected file {file} found in {subdir_path}")

        # Check if all expected directories are present in the output directory
        actual_subdirs = set(d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d)))
        expected_subdirs = set(expected_files.keys())
        missing_subdirs = expected_subdirs - actual_subdirs
        self.assertEqual(
            len(missing_subdirs),
            0,
            f"Expected directories not found in {output_dir}: {missing_subdirs}",
        )

        # Optionally, print a warning if there are additional directories
        additional_subdirs = actual_subdirs - expected_subdirs
        if additional_subdirs:
            print(f"Warning: Additional directories found in {output_dir}: {additional_subdirs}")
