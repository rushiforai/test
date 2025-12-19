import requests
from datetime import datetime
from utils import extract_code

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

def fetch(keywords):
    posts = []

    for kw in keywords:
        url = f"https://www.reddit.com/search.json?q={kw}&sort=new&limit=50"

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)

            # ✅ HARD CHECKS
            if r.status_code != 200:
                print(f"[reddit] HTTP {r.status_code}")
                continue

            if "application/json" not in r.headers.get("Content-Type", ""):
                print("[reddit] Non-JSON response (blocked)")
                continue

            data = r.json()

            for item in data.get("data", {}).get("children", []):
                p = item.get("data", {})
                text = (p.get("title", "") + " " + p.get("selftext", ""))
                print("[reddit] RAW TEXT:", text[:120])


                code = extract_code(text)
                if not code:
                    continue

                posts.append({
                    "platform": "reddit",
                    "code": code,
                    "url": "https://reddit.com" + p.get("permalink", ""),
                    "timestamp": datetime.utcfromtimestamp(
                        p.get("created_utc", 0)
                    ).isoformat() + "Z"
                })

        except Exception as e:
            print(f"[reddit] error: {e}")

    return posts
