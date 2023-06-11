from enum import Enum

class PluginType(Enum):
    DATA_SOURCE = "DATA_SOURCE"
    INTRO = "INTRO"
    SCRAPER = "SCRAPER"
    SEGMENT_WRITER = "SEGMENT_WRITER"
    SUMMARY = "SUMMARY"