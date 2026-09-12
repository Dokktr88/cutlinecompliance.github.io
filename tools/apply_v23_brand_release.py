#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_exact(path: Path, old: str, new: str, expected_min: int = 1) -> int:
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count < expected_min:
        raise SystemExit(f'{path.relative_to(ROOT)}: guarded target missing: {old[:120]}')
    path.write_text(text.replace(old, new), encoding='utf-8')
    return count

# Homepage brand/positioning refinements.
index = ROOT / 'index.html'
replace_exact(
    index,
    '<h1>Find weak signals before someone else finds the failure.</h1>',
    '<h1>See the system clearly. Build readiness deliberately.</h1>'
)
replace_exact(
    index,
    '<div><strong>Public-source intelligence</strong><span>Independent analysis built from documented, verifiable information.</span></div>',
    '<div><strong>Published intelligence</strong><span>Independent public-source analysis with visible sourcing, evidence, and reasoning.</span></div>'
)

# Cache-bust the brand-compliance stylesheet and move browser chrome to the light brand surface.
html_files = sorted(ROOT.rglob('*.html'))
for path in html_files:
    text = path.read_text(encoding='utf-8')
    if 'enhancements.css?v=1' not in text:
        raise SystemExit(f'{path.relative_to(ROOT)}: expected enhancements.css?v=1 reference missing')
    text = text.replace('enhancements.css?v=1', 'enhancements.css?v=2')
    text = re.sub(
        r'(<meta\s+name=["\']theme-color["\']\s+content=["\'])#07101d(["\']\s*/?>)',
        r'\1#FFFFFF\2',
        text,
        flags=re.I,
    )
    path.write_text(text, encoding='utf-8')

# Align installed-app/browser manifest surfaces to the current light visual system.
manifest_path = ROOT / 'manifest.webmanifest'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['background_color'] = '#FFFFFF'
manifest['theme_color'] = '#FFFFFF'
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

# Make the controlled visual system a permanent release gate.
validator_path = ROOT / 'tools' / 'validate_site.py'
validator = validator_path.read_text(encoding='utf-8')
site_js_gate = '''        if "/site.js?v=1" not in text:\n            errors.append(f"{rel}: missing shared site.js")\n'''
brand_gate = site_js_gate + '''        if "enhancements.css?v=2" not in text:\n            errors.append(f"{rel}: missing current brand stylesheet release enhancements.css?v=2")\n'''
if brand_gate not in validator:
    if validator.count(site_js_gate) != 1:
        raise SystemExit('tools/validate_site.py: shared-site gate anchor missing or ambiguous')
    validator = validator.replace(site_js_gate, brand_gate, 1)

sitemap_anchor = '''    sitemap_path = ROOT / "sitemap.xml"\n'''
brand_token_gate = '''    brand_css = (ROOT / "enhancements.css").read_text(encoding="utf-8")\n    for token in ("--cutline-red:#C8102E", "--cutline-black:#111111", "--cutline-light-gray:#F5F5F5"):\n        if token not in brand_css:\n            errors.append(f"enhancements.css: controlled Cutline brand token missing: {token}")\n\n'''
if 'controlled Cutline brand token missing' not in validator:
    if validator.count(sitemap_anchor) != 1:
        raise SystemExit('tools/validate_site.py: sitemap anchor missing or ambiguous')
    validator = validator.replace(sitemap_anchor, brand_token_gate + sitemap_anchor, 1)
validator_path.write_text(validator, encoding='utf-8')

print(f'Applied v2.3 brand release migration to {len(html_files)} HTML pages and strengthened the release gate.')
