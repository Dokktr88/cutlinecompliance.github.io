#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1) Keep Academy as the delivery platform; CRF is the Learn layer inside ARC.
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
old = '<div class="product-top"><span class="product-step">Platform — Learn</span><span class="status-pill pending">Active Build</span></div>'
new = '<div class="product-top"><span class="product-step">Education Platform</span><span class="status-pill pending">Active Build</span></div>'
if text.count(old) != 1:
    raise SystemExit(f"index.html: expected one Academy platform label, found {text.count(old)}")
index.write_text(text.replace(old, new, 1), encoding="utf-8")

# 2) Make the named architecture a permanent release-gate requirement.
validator = ROOT / "tools" / "validate_site.py"
text = validator.read_text(encoding="utf-8")
anchor = 'LEGAL_LINKS = ("/privacy.html", "/terms.html", "/accessibility.html")\n'
insert = '''LEGAL_LINKS = ("/privacy.html", "/terms.html", "/accessibility.html")
REQUIRED_POSITIONING = {
    "index.html": ("Applied Readiness Continuum (ARC)", "Learn. Diagnose. Interpret."),
    "services.html": ("Applied Readiness Continuum (ARC)", "Learn — CRF", "Diagnose — CRD", "Interpret — LIB"),
}
'''
if 'REQUIRED_POSITIONING = {' not in text:
    if text.count(anchor) != 1:
        raise SystemExit("validate_site.py: positioning insertion anchor missing or duplicated")
    text = text.replace(anchor, insert, 1)

loop_anchor = '''        for forbidden in FORBIDDEN_PUBLIC_TEXT:
            if forbidden in text:
                errors.append(f"{rel}: forbidden legacy or unconditional-tracking reference: {forbidden}")
'''
loop_insert = '''        for forbidden in FORBIDDEN_PUBLIC_TEXT:
            if forbidden in text:
                errors.append(f"{rel}: forbidden legacy or unconditional-tracking reference: {forbidden}")

        required_positioning = REQUIRED_POSITIONING.get(rel.as_posix(), ())
        for phrase in required_positioning:
            if phrase not in text:
                errors.append(f"{rel}: required Cutline positioning missing: {phrase}")
'''
if 'required_positioning = REQUIRED_POSITIONING.get' not in text:
    if text.count(loop_anchor) != 1:
        raise SystemExit("validate_site.py: validation insertion anchor missing or duplicated")
    text = text.replace(loop_anchor, loop_insert, 1)

validator.write_text(text, encoding="utf-8")
print("ARC architecture finalized and locked into release QA.")
