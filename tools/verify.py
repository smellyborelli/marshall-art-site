#!/usr/bin/env python3
"""Mechanical verification of the built site: metadata bounds, alt text, links,
JSON-LD syntax, NAP consistency, preview noindex, single H1 per page.

Run from the repo root:  python3 tools/verify.py
Requires: beautifulsoup4 (python3 -m pip install beautifulsoup4)

Note: this expects the PREVIEW build (noindex present). After cutover, flip the
noindex check to require the meta tag to be ABSENT.
"""
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup

SITE = Path(__file__).resolve().parent.parent
PAGES = {
    "home": ("index.html", "https://marshallartrestorations.com/"),
    "gallery": ("gallery/index.html", "https://marshallartrestorations.com/gallery/"),
    "gallery-1": ("gallery-1/index.html", "https://marshallartrestorations.com/gallery-1/"),
}

fails = []


def chk(cond, label, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}" + (f" — {detail}" if detail else ""))
    if not cond:
        fails.append(label)
    return cond


for key, (rel, canonical) in PAGES.items():
    p = SITE / rel
    soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    print(f"\n=== {key} ({rel}) ===")

    title = soup.title.get_text(strip=True) if soup.title else ""
    chk(len(title) <= 60, f"title ≤60 ({len(title)}): {title!r}")

    md = soup.find("meta", attrs={"name": "description"})
    d = md.get("content", "") if md else ""
    chk(0 < len(d) <= 155, f"meta description ≤155 ({len(d)})")

    h1s = soup.find_all("h1")
    chk(len(h1s) == 1, f"exactly one h1 ({len(h1s)})")

    robots = soup.find("meta", attrs={"name": "robots"})
    chk(bool(robots) and "noindex" in (robots.get("content", "")), "preview noindex present")

    can = soup.find("link", attrs={"rel": "canonical"})
    chk(bool(can) and can.get("href") == canonical, f"canonical == {canonical}")

    imgs = soup.find_all("img")
    bad_alt = [i.get("src", "?") for i in imgs if not (i.get("alt") or "").strip()]
    chk(not bad_alt, f"all {len(imgs)} images have alt text")

    no_dims = [i.get("src", "?") for i in imgs if not (i.get("width") and i.get("height"))]
    chk(not no_dims, "all images have width/height")

    missing_files = []
    for i in imgs:
        src = i.get("src", "")
        if src and not (p.parent / src).resolve().exists():
            missing_files.append(src)
    chk(not missing_files, "all image files exist on disk")

    bad_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        if not (p.parent / href).resolve().exists():
            bad_links.append(href)
    chk(not bad_links, "all internal links resolve")

print("\n=== JSON-LD (home) ===")
soup = BeautifulSoup((SITE / "index.html").read_text(encoding="utf-8"), "html.parser")
ld = soup.find("script", attrs={"type": "application/ld+json"})
if ld:
    try:
        data = json.loads(ld.string)
        chk(data.get("@type") == "ArtRestorationService", "JSON-LD @type correct")
    except Exception as e:
        chk(False, f"JSON-LD parses ({e})")
else:
    chk(False, "JSON-LD script present")

print("\n=== footer NAP ===")
for key, (rel, _) in PAGES.items():
    soup = BeautifulSoup((SITE / rel).read_text(encoding="utf-8"), "html.parser")
    foot = soup.find("footer")
    ft = foot.get_text(" ", strip=True) if foot else ""
    chk("Marshall Art Restorations" in ft and "New Gloucester, ME" in ft and "(402) 850-4040" in ft,
        f"{key} footer NAP")

print(f"\n{'='*50}\nRESULT: {'ALL PASS' if not fails else str(len(fails)) + ' FAILURES'}")
sys.exit(1 if fails else 0)
