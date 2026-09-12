#!/usr/bin/env python3
"""Apply deterministic Cutline website v2.1 hardening transforms.

This script exists so the same changes are applied consistently to every static page:
- remove unconditional Google Analytics bootstraps (site.js loads GA only after opt-in)
- remove legacy service-worker registration
- add shared enhancement CSS and site.js
- standardize Open Graph/Twitter metadata and social preview image
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GA_ID = "G-Z4KHLSPY1T"
OG_IMAGE = "https://cutlinecompliance.com/cutline-og-1200x630.png"

GA_RE = re.compile(
    rf"\s*(?:<!--\s*Google tag \(gtag\.js\)\s*-->\s*)?"
    rf"<script\s+async\s+src=[\"']https://www\.googletagmanager\.com/gtag/js\?id={re.escape(GA_ID)}[\"']></script>\s*"
    rf"<script>.*?gtag\([\"']config[\"']\s*,\s*[\"']{re.escape(GA_ID)}[\"']\s*\);.*?</script>\s*",
    re.DOTALL,
)

SW_BLOCK_RE = re.compile(
    r"\s*if\s*\(\s*['\"]serviceWorker['\"]\s+in\s+navigator\s*\)\s*"
    r"(?:\{\s*)?navigator\.serviceWorker\.register\(['\"]/sw\.js['\"]\)\.catch\(\(\)\s*=>\s*\{\}\);\s*(?:\}\s*)?",
    re.DOTALL,
)


def extract(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return html.unescape(match.group(1).strip()) if match else None


def attr(value: str) -> str:
    return html.escape(value, quote=True)


def ensure_social_meta(text: str, path: Path) -> str:
    if '<meta name="robots" content="noindex"' in text:
        return text

    title = extract(r"<title>(.*?)</title>", text)
    description = extract(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', text)
    canonical = extract(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']\s*/?>', text)
    if not title or not description or not canonical:
        return text

    social_type = "article" if "producer-direct-interstate-meat-commerce" in path.as_posix() else "website"

    if 'property="og:title"' not in text:
        block = f'''\n  <meta property="og:type" content="{social_type}" />
  <meta property="og:site_name" content="Cutline Compliance" />
  <meta property="og:title" content="{attr(title)}" />
  <meta property="og:description" content="{attr(description)}" />
  <meta property="og:url" content="{attr(canonical)}" />
  <meta property="og:image" content="{OG_IMAGE}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Cutline Compliance" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{attr(title)}" />
  <meta name="twitter:description" content="{attr(description)}" />
  <meta name="twitter:image" content="{OG_IMAGE}" />\n'''
        canonical_tag = re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', text, re.IGNORECASE)
        if canonical_tag:
            text = text[:canonical_tag.end()] + block + text[canonical_tag.end():]
    else:
        text = text.replace("https://cutlinecompliance.com/cutline-linkedin-banner-1584x396.png", OG_IMAGE)
        if 'property="og:site_name"' not in text:
            text = text.replace('<meta property="og:type"', '<meta property="og:site_name" content="Cutline Compliance" />\n  <meta property="og:type"', 1)
        if 'property="og:image:width"' not in text:
            text = re.sub(
                r'(<meta\s+property=["\']og:image["\'][^>]*>)',
                r'\1\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />\n  <meta property="og:image:alt" content="Cutline Compliance" />',
                text,
                count=1,
                flags=re.IGNORECASE,
            )
        if 'name="twitter:card"' not in text:
            marker = re.search(r'<meta\s+property=["\']og:image:alt["\'][^>]*>', text, re.IGNORECASE)
            if marker:
                block = f'''\n  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{attr(title)}" />
  <meta name="twitter:description" content="{attr(description)}" />
  <meta name="twitter:image" content="{OG_IMAGE}" />'''
                text = text[:marker.end()] + block + text[marker.end():]
        elif 'name="twitter:image"' not in text:
            twitter_card = re.search(r'<meta\s+name=["\']twitter:card["\'][^>]*>', text, re.IGNORECASE)
            if twitter_card:
                block = f'''\n  <meta name="twitter:title" content="{attr(title)}" />
  <meta name="twitter:description" content="{attr(description)}" />
  <meta name="twitter:image" content="{OG_IMAGE}" />'''
                text = text[:twitter_card.end()] + block + text[twitter_card.end():]

    return text


def transform(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = GA_RE.sub("\n", text)
    text = SW_BLOCK_RE.sub("\n", text)
    text = text.replace("https://cutlinecompliance.com/cutline-linkedin-banner-1584x396.png", OG_IMAGE)

    if "enhancements.css" not in text:
        css_link = '<link rel="stylesheet" href="/enhancements.css?v=1" />'
        style_match = re.search(r'<link\s+rel=["\']stylesheet["\'][^>]*styles\.css[^>]*>', text, re.IGNORECASE)
        if style_match:
            text = text[:style_match.end()] + "\n  " + css_link + text[style_match.end():]

    text = ensure_social_meta(text, path)

    if "/site.js?v=1" not in text:
        text = text.replace("</body>", '  <script defer src="/site.js?v=1"></script>\n</body>', 1)

    # Normalize accidental excess blank lines caused by removing legacy snippets.
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        if transform(path):
            changed.append(path.relative_to(ROOT).as_posix())

    print("Updated pages:")
    for item in changed:
        print(f" - {item}")
    if not changed:
        print(" - none (already hardened)")


if __name__ == "__main__":
    main()
