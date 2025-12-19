import requests
from datetime import datetime

def fetch(keywords):
    posts = []
    headers = {"User-Agent": "github-action-bot"}

    for kw in keywords:
        url = f"https://www.reddit.com/search.json?q={kw}&sort=new"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()

            for item in data["data"]["children"]:
                p = item["data"]
                posts.append({
                    "platform": "reddit",
                    "text": p.get("title", ""),
                    "url": "https://reddit.com" + p.get("permalink", ""),
                    "author": p.get("author", ""),
                    "timestamp": datetime.utcfromtimestamp(
                        p.get("created_utc", 0)
                    ).isoformat() + "Z",
                    "source": "reddit"
                })
        except Exception:
            pass

    return posts
