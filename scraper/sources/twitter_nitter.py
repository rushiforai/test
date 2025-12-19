import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils import extract_code

NITTER = "https://nitter.net"

def fetch(keywords):
    posts = []

    for kw in keywords:
        url = f"{NITTER}/search?f=tweets&q={kw}"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        for tweet in soup.select(".timeline-item"):
            text_el = tweet.select_one(".tweet-content")
            link_el = tweet.select_one("a.tweet-link")
            time_el = tweet.select_one("span.tweet-date a")

            if not (text_el and link_el and time_el):
                continue

            text = text_el.get_text(" ", strip=True)
            link = NITTER + link_el["href"]

            code = extract_code(text, link)
            if not code:
                continue

            timestamp = datetime.strptime(
                time_el["title"],
                "%b %d, %Y · %I:%M %p UTC"
            ).isoformat() + "Z"

            posts.append({
                "platform": "twitter",
                "code": code,
                "url": link,
                "timestamp": timestamp
            })

    return posts
