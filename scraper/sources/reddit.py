import requests
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch(keywords):
    posts = []

    for kw in keywords:
        url = f"https://www.reddit.com/search.json?q={kw}&sort=new&limit=25"
        print(f"[reddit] querying: {url}")

        r = requests.get(url, headers=HEADERS, timeout=15)
        print(f"[reddit] status: {r.status_code}")
        print(f"[reddit] content-type: {r.headers.get('Content-Type')}")

        if r.status_code != 200:
            continue

        if "json" not in r.headers.get("Content-Type", ""):
            print("[reddit] blocked (HTML returned)")
            print(r.text[:200])
            continue

        data = r.json()
        children = data.get("data", {}).get("children", [])
        print(f"[reddit] results: {len(children)}")

        for item in children[:3]:
            p = item.get("data", {})
            text = (p.get("title", "") + " " + p.get("selftext", ""))
            print("[reddit] sample text:", text[:120])

            posts.append({
                "platform": "reddit",
                "text": text,
                "url": "https://reddit.com" + p.get("permalink", ""),
                "timestamp": datetime.utcfromtimestamp(
                    p.get("created_utc", 0)
                ).isoformat() + "Z"
            })

    return posts
