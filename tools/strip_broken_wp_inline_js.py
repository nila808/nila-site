import re
from pathlib import Path

ROOT = Path(".")
FILE_GLOB = "**/index.html"

# Remove the entire broken block (it's WP editor utility code, not needed for the public site)
PATTERNS = [
    re.compile(
        r'\s*<script[^>]*\bid="nfd-wonder-blocks-utilities-js-after"[^>]*>.*?</script>\s*',
        re.DOTALL | re.IGNORECASE,
    ),
]

def strip_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8", errors="ignore")
    out = src
    for pat in PATTERNS:
        out = pat.sub("\n", out)
    if out != src:
        path.write_text(out, encoding="utf-8")
        return True
    return False

def main() -> None:
    changed = 0
    for p in ROOT.glob(FILE_GLOB):
        if strip_file(p):
            print(f"fixed: {p}")
            changed += 1
    print(f"\nDone. Files changed: {changed}")

if __name__ == "__main__":
    main()

