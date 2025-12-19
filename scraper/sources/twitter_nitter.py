import requests
from bs4 import BeautifulSoup
from datetime import datetime

from scraper.utils import extract_code

NITTER_MIRRORS = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch(keywords):
    results = []

    for base in NITTER_MIRRORS:
        for kw in keywords:
            search_url = f"{base}/search?f=tweets&q={kw}"
            print(f"[twitter] {search_url}")

            try:
                r = requests.get(search_url, headers=HEADERS, timeout=20)
                if r.status_code != 200:
                    continue

                soup = BeautifulSoup(r.text, "lxml")

                for item in soup.select(".timeline-item"):
                    text_el = item.select_one(".tweet-content")
                    link_el = item.select_one("a.tweet-link")
                    time_el = item.select_one("span.tweet-date a")

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

                    results.append({
                        "platform": "twitter",
                        "code": code,
                        "url": link,
                        "timestamp": timestamp
                    })

            except Exception as e:
                print(f"[twitter] error: {e}")
                continue

    return results
