import json
from pathlib import Path
from hashlib import sha256

from sources.twitter_nitter import fetch

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"

DATA_DIR.mkdir(exist_ok=True)

POSTS_FILE = DATA_DIR / "posts.json"
SEEN_FILE = DATA_DIR / "seen.json"

if not POSTS_FILE.exists():
    POSTS_FILE.write_text("[]")

if not SEEN_FILE.exists():
    SEEN_FILE.write_text("[]")

with open(CONFIG_DIR / "keywords.json") as f:
    keywords = json.load(f)["keywords"]

seen = set(json.loads(SEEN_FILE.read_text()))
existing = json.loads(POSTS_FILE.read_text())

new_posts = []

for post in fetch(keywords):
    pid = sha256((post["platform"] + post["url"] + post["code"]).encode()).hexdigest()
    if pid in seen:
        continue

    seen.add(pid)
    post["id"] = pid
    new_posts.append(post)

all_posts = new_posts + existing
all_posts.sort(key=lambda x: x["timestamp"], reverse=True)
all_posts = all_posts[:500]

POSTS_FILE.write_text(json.dumps(all_posts, indent=2))
SEEN_FILE.write_text(json.dumps(list(seen), indent=2))

print(f"[run] New posts added: {len(new_posts)}")
print(f"[run] Total stored posts: {len(all_posts)}")
