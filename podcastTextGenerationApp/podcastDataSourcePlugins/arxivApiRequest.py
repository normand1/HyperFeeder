import feedparser
from datetime import datetime, timedelta

# Define the date one week ago
one_week_ago = datetime.now() - timedelta(weeks=1)

# Fetch recent AI papers
feed = feedparser.parse(
    "https://export.arxiv.org/api/query?search_query=all:artificial%20intelligence&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100"
)

# Filter for entries from the past week
recent_papers = [
    entry
    for entry in feed.entries
    if datetime(*entry.published_parsed[:6]) > one_week_ago
]

# Print the titles of the recent papers
for paper in recent_papers:
    print(paper)
