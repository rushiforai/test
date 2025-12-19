import requests
from bs4 import BeautifulSoup
from datetime import datetime

SEARCH_URL = "https://duckduckgo.com/html/"

def fetch(keywords):
    posts = []

    for kw in keywords:
        query = f'site:tiktok.com OR site:facebook.com "{kw}"'
        try:
            r = requests.post(
                SEARCH_URL,
                data={"q": query},
                timeout=10
            )
            soup = BeautifulSoup(r.text, "lxml")

            for result in soup.select(".result"):
                link = result.select_one("a.result__a")
                if not link:
                    continue

                url = link["href"]
                platform = "tiktok" if "tiktok.com" in url else "facebook"

                posts.append({
                    "platform": platform,
                    "text": link.get_text(strip=True),
                    "url": url,
                    "author": "",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "source": "serp"
                })
        except Exception:
            pass

    return posts
