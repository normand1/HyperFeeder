import re
import codecs
from bs4 import BeautifulSoup


class TextFilteringUtils:
    @staticmethod
    def remove_links(text: str) -> str:
        """
        Removes markdown-style links from the input text.

        Args:
            text (str): The input text containing links to be removed

        Returns:
            str: The text with all markdown links removed
        """
        # Pattern matches markdown links in the format [optional-text](url)
        link_pattern = r"\[([^\]]*)\]\([^)]+\)"

        # Replace links with just the text inside brackets (or empty string if no text)
        cleaned_text = re.sub(link_pattern, r"\1", text)
        return cleaned_text

    @staticmethod
    def cleanupStorySummary(story) -> str:
        summaryText = story
        summaryText = summaryText.replace("\\", "")
        summaryText = summaryText.replace("   ", "")
        summaryText = summaryText.replace("  ", "")
        return summaryText

    @staticmethod
    def cleanText(text: str) -> str:
        """
        Cleans up the input text by removing or replacing unwanted characters and formatting.
        """

        # 1. Decode unicode escape sequences
        try:
            text = codecs.decode(text, "unicode_escape")
        except Exception:
            pass

        # 2. Replace escaped single and double quotes with actual quotes
        text = text.replace("\\'", "'").replace('\\"', '"')

        # 3. Remove other common escape sequences
        escape_sequences = {
            r"\\": "\\",
            r"\n": " ",
            r"\t": " ",
            r"\r": " ",
        }
        for esc, char in escape_sequences.items():
            text = text.replace(esc, char)

        # 4. Remove asterisks for markdown formatting
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)

        # 5. Remove numbers with periods used for list formatting
        text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

        # 6. Remove markdown links but keep link text
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

        # 7. Remove markdown images
        text = re.sub(r"!\[([^\]]*)\]\([^\)]+\)", "", text)

        # 8. Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        # 9. Remove inline code snippets
        text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)

        # 10. Replace multiple whitespace with single space
        text = re.sub(r"\s+", " ", text)

        # 11. Strip leading/trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def clean_scraped_text(html_content: str) -> str:
        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Convert all tags to text
        text = soup.get_text(separator="\n")

        # Remove extraneous whitespace
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Define patterns of extraneous content
        # These are common words or phrases found in navigation, disclaimers, and ads
        extraneous_patterns = [
            r"^(Subscribe|Sign In|CREATE FREE ACCOUNT|Markets|Business|Investing|Tech|Politics|Video|Watchlist|Menu)$",
            r"Privacy Policy",
            r"Ad Choices",
            r"Contact",
            r"Site Map",
            r"Select Personal Finance",
            r"Select Shopping",
            r"Help",
            r"Terms of Service",
            r"Your Privacy Choices",
            r"Data is a real-time snapshot",
            r"Promoted Links",
            r"Sponsored Links",
            r"Read More",
            r"© \d{4} CNBC LLC",
            r"by Taboola",
            r"[\[\(].*?[\]\)]",  # Removes bracketed link references if needed
        ]

        # Any line heavily filled with links (heuristic: 'http' repeats)
        def is_link_heavy(l):
            return l.count("http") > 2

        # Filter lines
        filtered_lines = []
        for line in lines:
            # Skip link-heavy lines
            if is_link_heavy(line):
                continue
            # Skip lines matching extraneous patterns
            if any(re.search(p, line, re.IGNORECASE) for p in extraneous_patterns):
                continue
            # Skip lines that are just menu items or repeated anchor texts
            if re.match(r"^\W*$", line):
                continue
            filtered_lines.append(line)

        # Join and then further trim unnecessary blank lines
        cleaned_text = "\n".join(filtered_lines)
        cleaned_text = re.sub(r"\n{2,}", "\n\n", cleaned_text).strip()

        return cleaned_text
