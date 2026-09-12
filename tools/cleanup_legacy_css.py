#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "styles.css"

html_text = "\n".join(
    p.read_text(encoding="utf-8")
    for p in ROOT.rglob("*.html")
    if ".git" not in p.parts
)

# Each large legacy section is removed only if its distinctive classes are absent
# from every current HTML page. Failing the guard aborts the cleanup rather than
# guessing about a live layout dependency.
sections = [
    (
        "use cases + LinkedIn embeds",
        ["use-case-grid", "use-case-card", "linkedin-grid", "linkedin-embed-card", "linkedin-actions"],
        r"/\* USE CASES \*/.*?(?=/\* WHO \*/)",
    ),
    (
        "readiness popup",
        ["readiness-popup", "readiness-popup-card", "popup-actions", "popup-open"],
        r"/\* READINESS POPUP \*/.*?(?=/\* FOOTER \*/)",
    ),
    (
        "embedded form",
        ["form-embed"],
        r"/\* EMBEDDED FORM \*/.*?(?=/\* ELIGIBILITY / SCOPE NOTICE \*/)",
    ),
    (
        "floating CRD CTA",
        ["cta-float"],
        r"/\* FLOATING CRD CTA \*/.*\Z",
    ),
]

text = CSS.read_text(encoding="utf-8")
original = text

for label, classes, pattern in sections:
    live = [cls for cls in classes if re.search(rf'class=["\'][^"\']*\b{re.escape(cls)}\b', html_text)]
    if live:
        raise SystemExit(f"Refusing to remove {label}; live classes found: {', '.join(live)}")
    text, count = re.subn(pattern, "", text, flags=re.S)
    if count != 1:
        raise SystemExit(f"Expected exactly one {label} CSS section, found {count}")

# Remove standalone founder rules only after proving founder-card is not used.
if re.search(r'class=["\'][^"\']*\bfounder-card\b', html_text):
    raise SystemExit("Refusing to remove founder-card CSS; class is still live")
text = re.sub(r"\n\.founder-card\{.*?\n\}\n", "\n", text, flags=re.S)
text = re.sub(r"\n\.founder-card img\{.*?\n\}\n", "\n", text, flags=re.S)
text = re.sub(r"\n\.founder-card h3\{.*?\n\}\n", "\n", text, flags=re.S)
text = re.sub(r"\n\.founder-card p\{.*?\n\}\n", "\n", text, flags=re.S)

text = re.sub(r"\n{4,}", "\n\n\n", text).rstrip() + "\n"

if text == original:
    raise SystemExit("Cleanup produced no changes")

CSS.write_text(text, encoding="utf-8")
print(f"styles.css reduced from {len(original):,} to {len(text):,} characters")
