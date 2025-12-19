import json
from pathlib import Path
from configparser import ConfigParser

from sources.reddit import fetch as reddit
from sources.twitter_nitter import fetch as twitter
from sources.serp import fetch as serp

from normalize import normalize
from deduplicate import load_seen, save_seen

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

with open("config/keywords.json") as f:
    keywords = json.load(f)["keywords"]

seen = load_seen()
all_posts = []

for source in (reddit, twitter, serp):
    for post in source(keywords):
        post = normalize(post)
        if post["id"] not in seen:
            seen.add(post["id"])
            all_posts.append(post)

all_posts.sort(key=lambda x: x["timestamp"], reverse=True)

(Path("data/posts.json")).write_text(
    json.dumps(all_posts, indent=2)
)

save_seen(seen)
