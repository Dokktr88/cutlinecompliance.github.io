#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LEGAL = '''
    <div class="container legal-footer-links">
      <a href="/privacy.html">Privacy</a>
      <a href="/terms.html">Terms of Use</a>
      <a href="/accessibility.html">Accessibility</a>
      <button type="button" class="privacy-choice-button" data-reset-analytics>Privacy choices</button>
    </div>
'''

INLINE_SCRIPT = re.compile(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', re.I | re.S)


def clean_inline_script(match: re.Match[str]) -> str:
    attrs, body = match.group(1), match.group(2)
    if 'application/ld+json' in attrs.lower():
        return match.group(0)
    if "document.getElementById('yr')" not in body and 'document.getElementById("yr")' not in body:
        return match.group(0)
    if 'menu-toggle' not in body:
        return match.group(0)

    # The policy-intelligence page also contains report-specific analytics and
    # section-navigation behavior. Preserve that page-specific code while
    # removing the duplicated global year/menu logic.
    if 'pdimcAnalytics' in body:
        marker = "document.querySelectorAll('.section-nav"
        pos = body.find(marker)
        if pos == -1:
            raise SystemExit('Could not locate PDIMC section-navigation marker')
        preserved = body[pos:].strip()
        return f'<script>\n{preserved}\n</script>'

    # All other matching inline blocks are the old shared year/menu/anchor code.
    return ''


def update_html(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text

    if 'legal-footer-links' not in text:
        if '</footer>' not in text:
            raise SystemExit(f'{path}: no footer found')
        text = text.replace('</footer>', LEGAL + '  </footer>', 1)

    text = INLINE_SCRIPT.sub(clean_inline_script, text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def update_site_js() -> bool:
    path = ROOT / 'site.js'
    text = path.read_text(encoding='utf-8')
    original = text
    needle = "document.querySelectorAll('a[href^=\"#\"]').forEach((link) => {\n      link.addEventListener"
    replacement = "document.querySelectorAll('a[href^=\"#\"]').forEach((link) => {\n      if (link.closest('.section-nav')) return;\n      link.addEventListener"
    if replacement not in text:
        if needle not in text:
            raise SystemExit('site.js: expected smooth-anchor pattern not found')
        text = text.replace(needle, replacement, 1)
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob('*.html')):
        if '.git' in path.parts:
            continue
        if update_html(path):
            changed.append(path.relative_to(ROOT).as_posix())
    if update_site_js():
        changed.append('site.js')
    print('Final-polish files changed:')
    for item in changed:
        print(f' - {item}')


if __name__ == '__main__':
    main()
