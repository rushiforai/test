import requests
from bs4 import BeautifulSoup
from datetime import datetime

NITTER = "https://nitter.net"

def fetch(keywords):
    posts = []

    for kw in keywords:
        url = f"{NITTER}/search?f=tweets&q={kw}"
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "lxml")

            for tweet in soup.select(".timeline-item"):
                text = tweet.select_one(".tweet-content")
                link = tweet.select_one("a.tweet-link")
                time = tweet.select_one("span.tweet-date a")

                if not (text and link and time):
                    continue

                timestamp = time["title"]

                posts.append({
                    "platform": "twitter",
                    "text": text.get_text(strip=True),
                    "url": NITTER + link["href"],
                    "author": "",
                    "timestamp": datetime.strptime(
                        timestamp, "%b %d, %Y · %I:%M %p UTC"
                    ).isoformat() + "Z",
                    "source": "nitter"
                })
        except Exception:
            pass

    return posts
