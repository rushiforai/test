import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils import extract_code

NITTERS = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch(keywords):
    posts = []

    for base in NITTERS:
        for kw in keywords:
            url = f"{base}/search?f=tweets&q={kw}"
            print(f"[twitter] {url}")

            try:
                r = requests.get(url, headers=HEADERS, timeout=20)
                if r.status_code != 200:
                    continue

                soup = BeautifulSoup(r.text, "lxml")

                for tweet in soup.select(".timeline-item"):
                    text_el = tweet.select_one(".tweet-content")
                    link_el = tweet.select_one("a.tweet-link")
                    time_el = tweet.select_one("span.tweet-date a")

                    if not (text_el and link_el and time_el):
                        continue

                    text = text_el.get_text(" ", strip=True)
                    link = base + link_el["href"]

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

            except Exception:
                continue

    return posts
