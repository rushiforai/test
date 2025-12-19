import re

CODE_REGEX = re.compile(
    r'(?:\bcode\b[\s:=()]*|[?&]code=)([A-Z0-9]{6,12})',
    re.IGNORECASE
)

def extract_code(text, url=""):
    match = CODE_REGEX.search(text + " " + url)
    if match:
        return match.group(1).upper()
    return None
