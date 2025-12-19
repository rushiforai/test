import re

CODE_REGEX = re.compile(
    r'(?:\bcode\b[\s:=()]*|[?&]code=|\breferral\b[\s:=()]*)'
    r'([A-Z0-9]{6,12})',
    re.IGNORECASE
)

def extract_code(text, url=""):
    combined = f"{text} {url}"
    match = CODE_REGEX.search(combined)
    if match:
        return match.group(1).upper()
    return None
