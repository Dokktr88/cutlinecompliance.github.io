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
    if '/enhancements.css?v=1' not in text:
        raise SystemExit(f'{path.relative_to(ROOT)}: expected enhancements.css?v=1 reference missing')
    text = text.replace('/enhancements.css?v=1', '/enhancements.css?v=2')
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

print(f'Applied v2.3 brand release migration to {len(html_files)} HTML pages.')
