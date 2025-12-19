
import json
from pathlib import Path
from sources.reddit import fetch as reddit
from sources.twitter_nitter import fetch as twitter

DATA = Path("data")
DATA.mkdir(exist_ok=True)

SEEN_FILE = DATA_DIR / "seen.json"

# ✅ Ensure seen.json always exists
if not SEEN_FILE.exists():
    SEEN_FILE.write_text("[]")

with open("config/keywords.json") as f:
    keywords = json.load(f)["keywords"]

posts = []
posts.extend(reddit(keywords))
posts.extend(twitter(keywords))

posts.sort(key=lambda x: x["timestamp"], reverse=True)

(DATA / "posts.json").write_text(
    json.dumps(posts, indent=2)
)
