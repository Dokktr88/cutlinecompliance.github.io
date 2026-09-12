#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

css_path = ROOT / 'enhancements.css'
css = css_path.read_text(encoding='utf-8')
old = 'font-family:Arial,Helvetica,system-ui,-apple-system,"Segoe UI",sans-serif;'
new = 'font-family:Aptos,Arial,Helvetica,system-ui,-apple-system,"Segoe UI",sans-serif;'
if css.count(old) != 1:
    raise SystemExit(f'enhancements.css: expected one controlled font stack, found {css.count(old)}')
css_path.write_text(css.replace(old, new, 1), encoding='utf-8')

validator_path = ROOT / 'tools' / 'validate_site.py'
validator = validator_path.read_text(encoding='utf-8')
anchor = '''    for token in ("--cutline-red:#C8102E", "--cutline-black:#111111", "--cutline-light-gray:#F5F5F5"):\n        if token not in brand_css:\n            errors.append(f"enhancements.css: controlled Cutline brand token missing: {token}")\n'''
replacement = '''    for token in ("--cutline-red:#C8102E", "--cutline-black:#111111", "--cutline-light-gray:#F5F5F5", 'font-family:Aptos,Arial,Helvetica,system-ui,-apple-system,"Segoe UI",sans-serif;'):\n        if token not in brand_css:\n            errors.append(f"enhancements.css: controlled Cutline brand token missing: {token}")\n'''
if validator.count(anchor) != 1:
    raise SystemExit('tools/validate_site.py: controlled brand token gate anchor missing or ambiguous')
validator_path.write_text(validator.replace(anchor, replacement, 1), encoding='utf-8')

print('Typography hotfix applied and release gate strengthened.')
