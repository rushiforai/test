import json
from pathlib import Path

from sources.reddit import fetch as fetch_reddit
from sources.twitter_nitter import fetch as fetch_twitter
from normalize import normalize
from deduplicate import load_seen, save_seen

# =========================
# Paths & directories
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"

DATA_DIR.mkdir(exist_ok=True)

POSTS_FILE = DATA_DIR / "posts.json"
SEEN_FILE = DATA_DIR / "seen.json"

# =========================
# Ensure files exist
# =========================
if not POSTS_FILE.exists():
    POSTS_FILE.write_text("[]")

if not SEEN_FILE.exists():
    SEEN_FILE.write_text("[]")

# =========================
# Load keywords
# =========================
with open(CONFIG_DIR / "keywords.json", "r") as f:
    keywords = json.load(f)["keywords"]

# =========================
# Load seen IDs
# =========================
seen = load_seen()
new_posts = []

# =========================
# Fetch from sources
# =========================
SOURCES = [
    fetch_reddit,
    fetch_twitter,
]

for source in SOURCES:
    try:
        posts = source(keywords)
    except Exception as e:
        print(f"[run] source failed: {source.__name__} → {e}")
        continue

    for post in posts:
        try:
            post = normalize(post)
        except Exception:
            continue

        if post["id"] in seen:
            continue

        seen.add(post["id"])
        new_posts.append(post)

# =========================
# Load existing posts
# =========================
try:
    existing_posts = json.loads(POSTS_FILE.read_text())
except Exception:
    existing_posts = []

# =========================
# Merge + sort (latest first)
# =========================
all_posts = new_posts + existing_posts
all_posts.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

# Optional: cap size to keep repo small
MAX_POSTS = 500
all_posts = all_posts[:MAX_POSTS]

# =========================
# Write outputs
# =========================
POSTS_FILE.write_text(json.dumps(all_posts, indent=2))
save_seen(seen)

# =========================
# Logging (for Actions)
# =========================
print(f"[run] New posts added: {len(new_posts)}")
print(f"[run] Total stored posts: {len(all_posts)}")
print("[run] Done.")
