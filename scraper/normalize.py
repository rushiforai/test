import hashlib

def normalize(post):
    raw = (post["platform"] + post["url"] + post["text"]).encode()
    post["id"] = hashlib.sha256(raw).hexdigest()
    return post
