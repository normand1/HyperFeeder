import re


def strip_xml_tags(text):
    """
    Remove XML tags from the given text using regular expressions.
    """
    clean = re.compile(r"<[^>]+>")
    return re.sub(clean, "", text)
