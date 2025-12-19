import json
from pathlib import Path

SEEN_FILE = Path("data/seen.json")

def load_seen():
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()

def save_seen(seen):
    SEEN_FILE.write_text(json.dumps(list(seen), indent=2))
