import requests
from datetime import datetime
from utils import extract_code

PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search/submission/"

def fetch(keywords):
    posts = []

    for kw in keywords:
        url = (
            f"{PUSHSHIFT_URL}"
            f"?q={kw}"
            f"&size=50"
            f"&sort=desc"
            f"&sort_type=created_utc"
        )

        print(f"[pushshift] query: {kw}")

        try:
            r = requests.get(url, timeout=20)
            if r.status_code != 200:
                print(f"[pushshift] HTTP {r.status_code}")
                continue

            data = r.json().get("data", [])
            print(f"[pushshift] results: {len(data)}")

            for p in data:
                text = (p.get("title", "") + " " + p.get("selftext", "")).strip()

                code = extract_code(text)
                if not code:
                    continue

                posts.append({
                    "platform": "reddit",
                    "code": code,
                    "url": p.get("full_link") or p.get("url", ""),
                    "timestamp": datetime.utcfromtimestamp(
                        p.get("created_utc", 0)
                    ).isoformat() + "Z"
                })

        except Exception as e:
            print(f"[pushshift] error: {e}")

    return posts
