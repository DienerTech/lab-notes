"""Pre-publish check: fail if any tracked text file, or any image metadata, contains a private pattern.

    python tools/scrub_check.py            # scans the repo; exits 1 on any hit

Patterns come from built-in generic rules (API keys, local user paths, private LAN IPs, e-mail
addresses) plus an optional, git-ignored `.scrub-patterns.local` file (one regex per line) for your own
names, org IDs, hostnames and similar. That file never gets committed, so the patterns themselves stay
private. Image files are checked for embedded EXIF/XMP/text chunks.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERIC = [
    r"sk-[A-Za-z0-9_\-]{16,}",                # API keys
    r"\borg-[A-Za-z0-9]{16,}",                # OpenAI org IDs
    r"[A-Za-z]:[\\/]+Users[\\/]",             # Windows user paths
    r"/home/[a-z0-9_\-]+/",                   # Linux home paths
    r"\b192\.168\.\d+\.\d+\b", r"\b10\.\d+\.\d+\.\d+\b",
    r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[a-z]{2,}",
]
ALLOW = [r"noreply@", r"@remotion", r"@fontsource", r"@types"]
TEXT = {".md", ".py", ".ts", ".tsx", ".json", ".yml", ".yaml", ".txt", ".js", ".mjs", ".html", ".css", ".toml"}
IMG = {".webp", ".png", ".jpg", ".jpeg", ".gif"}


def main():
    pats = list(GENERIC)
    local = ROOT / ".scrub-patterns.local"
    if local.exists():
        pats += [l.strip() for l in local.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    rx = [re.compile(p, re.I) for p in pats]; allow = [re.compile(p, re.I) for p in ALLOW]
    hits = []
    for f in ROOT.rglob("*"):
        if not f.is_file() or ".git" in f.parts or "node_modules" in f.parts or f.name == ".scrub-patterns.local": continue
        if f.suffix.lower() in TEXT:
            for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                for r in rx:
                    for m in r.finditer(line):
                        if not any(a.search(m.group(0)) for a in allow):
                            hits.append(f"{f.relative_to(ROOT)}:{n}: matches /{r.pattern}/")
        elif f.suffix.lower() in IMG:
            data = f.read_bytes()
            for tag in (b"Exif", b"XMP ", b"<x:xmpmeta", b"tEXt", b"iTXt"):
                if tag in data[:65536]:
                    hits.append(f"{f.relative_to(ROOT)}: embedded metadata chunk {tag!r}")
            for r in rx[len(GENERIC):]:
                if re.search(r.pattern.encode(), data, re.I):
                    hits.append(f"{f.relative_to(ROOT)}: binary contains /{r.pattern}/")
    for h in hits: print(h)
    print(f"scrub_check: {len(hits)} issue(s)" + ("" if local.exists() else "  (no .scrub-patterns.local found; generic rules only)"))
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
