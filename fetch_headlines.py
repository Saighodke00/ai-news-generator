import feedparser
from datetime import datetime

RSS_FEED_URL = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"
HEADLINE_COUNT = 5

def fetch_headlines(url=RSS_FEED_URL, count=HEADLINE_COUNT):
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            print("No news found at the moment.")
            return []

        headlines = []
        for entry in feed.entries[:count]:
            title = entry.title.strip()
            sentence = f"Headline {len(headlines)+1}: {title}"
            headlines.append(sentence)

        return headlines

    except Exception as e:
        print(f"Couldn't fetch headlines right now. Error: {e}")
        return []

if __name__ == "__main__":
    headlines = fetch_headlines()
    for line in headlines:
        print(line)
