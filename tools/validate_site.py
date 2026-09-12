#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://cutlinecompliance.com"
FORBIDDEN_PUBLIC_TEXT = (
    "Jesse E. Stanley",
    "16+ years",
    "Blue Shirt White Background3v3.jpg",
    "Learning Hub",
    "cutline-linkedin-banner-1584x396.png",
    "googletagmanager.com/gtag/js",
    "serviceWorker.register('/sw.js')",
)
LEGAL_LINKS = ("/privacy.html", "/terms.html", "/accessibility.html")
PRODUCT_ACRONYMS = {
    "ARC": "Applied Readiness Continuum (ARC)",
    "CRF": "Compliance Readiness Fundamentals (CRF)",
    "CRD": "Compliance Readiness Diagnostic (CRD)",
    "LIB": "Leadership Intelligence Brief (LIB)",
}
REQUIRED_POSITIONING = {
    "index.html": ("Applied Readiness Continuum (ARC)", "Learn. Diagnose. Interpret."),
    "services.html": ("APPLIED READINESS CONTINUUM (ARC)", "Learn — CRF", "Diagnose — CRD", "Interpret — LIB"),
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[tuple[str, dict[str, str]]] = []
        self.assets: list[str] = []
        self.images: list[dict[str, str]] = []
        self.meta_name: dict[str, str] = {}
        self.meta_property: dict[str, str] = {}
        self.canonicals: list[str] = []
        self.h1_count = 0
        self.title_count = 0
        self.skip_link = False

    def handle_starttag(self, tag: str, attrs_raw):
        attrs = {k: (v or "") for k, v in attrs_raw}
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append((attrs["href"], attrs))
            if attrs["href"] == "#main" and "skip" in attrs.get("class", "").split():
                self.skip_link = True
        if tag == "img":
            self.images.append(attrs)
            if attrs.get("src"):
                self.assets.append(attrs["src"])
        if tag == "script" and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("href"):
            rel = set(attrs.get("rel", "").lower().split())
            if "canonical" in rel:
                self.canonicals.append(attrs["href"])
            elif rel.intersection({"stylesheet", "icon", "manifest", "apple-touch-icon"}):
                self.assets.append(attrs["href"])
        if tag == "meta":
            if attrs.get("name"):
                self.meta_name[attrs["name"].lower()] = attrs.get("content", "")
            if attrs.get("property"):
                self.meta_property[attrs["property"].lower()] = attrs.get("content", "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_count += 1


def local_target(source: Path, raw_url: str) -> tuple[Path | None, str]:
    parts = urlsplit(raw_url)
    if parts.scheme or parts.netloc or raw_url.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None, parts.fragment
    url_path = parts.path
    fragment = parts.fragment
    if not url_path:
        return source, fragment
    if url_path.startswith("/"):
        target = ROOT / url_path.lstrip("/")
    else:
        target = source.parent / url_path
    target = target.resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return target, fragment
    if url_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target, fragment


def parse_page(path: Path) -> tuple[PageParser, str]:
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    return parser, text


def validate_json_ld(path: Path, text: str, errors: list[str]) -> None:
    pattern = re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', re.I | re.S)
    for idx, payload in enumerate(pattern.findall(text), start=1):
        try:
            json.loads(html.unescape(payload).strip())
        except Exception as exc:
            errors.append(f"{path}: invalid JSON-LD block {idx}: {exc}")


def main() -> int:
    errors: list[str] = []
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    parsed: dict[Path, PageParser] = {}

    for path in pages:
        parser, text = parse_page(path)
        parsed[path.resolve()] = parser
        rel = path.relative_to(ROOT)
        public = path.name != "404.html"

        duplicates = [value for value, count in Counter(parser.ids).items() if count > 1]
        if duplicates:
            errors.append(f"{rel}: duplicate ids: {', '.join(duplicates)}")

        if public:
            if parser.title_count != 1:
                errors.append(f"{rel}: expected exactly one <title>, found {parser.title_count}")
            if not parser.meta_name.get("description"):
                errors.append(f"{rel}: missing meta description")
            if len(parser.canonicals) != 1:
                errors.append(f"{rel}: expected exactly one canonical URL")
            if parser.h1_count != 1:
                errors.append(f"{rel}: expected exactly one h1, found {parser.h1_count}")
            if not parser.skip_link:
                errors.append(f"{rel}: missing skip-to-content link")
            for key in ("og:title", "og:description", "og:url", "og:image"):
                if not parser.meta_property.get(key):
                    errors.append(f"{rel}: missing {key}")
            for key in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
                if not parser.meta_name.get(key):
                    errors.append(f"{rel}: missing {key}")

        if "/site.js?v=1" not in text:
            errors.append(f"{rel}: missing shared site.js")
        if "enhancements.css?v=2" not in text:
            errors.append(f"{rel}: missing current brand stylesheet release enhancements.css?v=2")
        if "legal-footer-links" not in text:
            errors.append(f"{rel}: legal footer must be present in static HTML")
        for legal_href in LEGAL_LINKS:
            if f'href="{legal_href}"' not in text:
                errors.append(f"{rel}: static legal footer missing {legal_href}")
        if "data-reset-analytics" not in text:
            errors.append(f"{rel}: static privacy-choice control missing")
        if re.search(r"document\.querySelector\(['\"]\.menu-toggle['\"]\)", text):
            errors.append(f"{rel}: duplicated inline menu behavior; use site.js")

        for forbidden in FORBIDDEN_PUBLIC_TEXT:
            if forbidden in text:
                errors.append(f"{rel}: forbidden legacy or unconditional-tracking reference: {forbidden}")

        required_positioning = REQUIRED_POSITIONING.get(rel.as_posix(), ())
        for phrase in required_positioning:
            if phrase not in text:
                errors.append(f"{rel}: required Cutline positioning missing: {phrase}")

        body_source = text.split("<body", 1)[1] if "<body" in text else text
        body_lower = body_source.lower()
        for acronym, definition in PRODUCT_ACRONYMS.items():
            match = re.search(rf"\b{re.escape(acronym)}\b", body_source)
            if not match:
                continue
            definition_index = body_lower.find(definition.lower())
            if definition_index == -1 or definition_index > match.start():
                errors.append(f"{rel}: {acronym} appears before it is introduced as '{definition}'")

        for img in parser.images:
            if "alt" not in img:
                errors.append(f"{rel}: image missing alt attribute: {img.get('src', '<unknown>')}")

        for href, attrs in parser.links:
            if attrs.get("target") == "_blank" and "noopener" not in attrs.get("rel", "").lower().split():
                errors.append(f"{rel}: target=_blank link missing rel=noopener: {href}")

        validate_json_ld(rel, text, errors)

    for source_resolved, parser in parsed.items():
        source = source_resolved
        rel = source.relative_to(ROOT.resolve())
        for raw in parser.assets:
            target, _ = local_target(source, raw)
            if target is not None and not target.exists():
                errors.append(f"{rel}: missing local asset {raw}")
        for href, _attrs in parser.links:
            target, fragment = local_target(source, href)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{rel}: broken local link {href}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target.resolve())
                if target_parser and fragment not in set(target_parser.ids):
                    errors.append(f"{rel}: missing fragment #{fragment} in {target.relative_to(ROOT.resolve())}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"} and path.stat().st_size > 2_000_000:
            errors.append(f"{path.relative_to(ROOT)}: image exceeds 2 MB ({path.stat().st_size:,} bytes)")

    brand_css = (ROOT / "enhancements.css").read_text(encoding="utf-8")
    for token in ("--cutline-red:#C8102E", "--cutline-black:#111111", "--cutline-light-gray:#F5F5F5", 'font-family:Aptos,Arial,Helvetica,system-ui,-apple-system,"Segoe UI",sans-serif;'):
        if token not in brand_css:
            errors.append(f"enhancements.css: controlled Cutline brand token missing: {token}")

    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        errors.append("sitemap.xml: missing")
    else:
        try:
            root = ET.parse(sitemap_path).getroot()
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = root.findall("sm:url", ns)
            sitemap_locs = {node.findtext("sm:loc", default="", namespaces=ns) for node in urls}
            for node in urls:
                if not node.findtext("sm:lastmod", default="", namespaces=ns):
                    errors.append("sitemap.xml: every URL must include lastmod")
            for path_resolved, parser in parsed.items():
                page = Path(path_resolved)
                if page.name == "404.html" or not parser.canonicals:
                    continue
                canonical = parser.canonicals[0]
                if canonical.startswith(SITE) and canonical not in sitemap_locs:
                    errors.append(f"sitemap.xml: missing canonical {canonical}")
        except Exception as exc:
            errors.append(f"sitemap.xml: invalid XML: {exc}")

    if errors:
        print("SITE QA FAILED")
        for item in errors:
            print(f" - {item}")
        return 1

    print(f"SITE QA PASSED: {len(pages)} HTML pages validated with no release-blocking findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
