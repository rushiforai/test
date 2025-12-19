import requests
from datetime import datetime
from utils import extract_code

def fetch(keywords):
    posts = []
    headers = {"User-Agent": "github-action-bot"}

    for kw in keywords:
        url = f"https://www.reddit.com/search.json?q={kw}&sort=new"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        for item in data["data"]["children"]:
            p = item["data"]
            text = (p.get("title", "") + " " + p.get("selftext", ""))
            code = extract_code(text)

            if not code:
                continue

            posts.append({
                "platform": "reddit",
                "code": code,
                "url": "https://reddit.com" + p.get("permalink", ""),
                "timestamp": datetime.utcfromtimestamp(
                    p["created_utc"]
                ).isoformat() + "Z"
            })

    return posts
