#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

replacements = {
    ROOT / "index.html": [
        (
            '<div><strong>Applied readiness tools</strong><span>Structured products for learning, diagnostic visibility, and stronger internal discussion.</span></div>',
            '<div><strong>Applied Readiness Continuum (ARC)</strong><span>Cutline\'s learn → diagnose → interpret architecture for organizational readiness.</span></div>',
        ),
        (
            '<p class="eyebrow">CUTLINE PRODUCTS & PLATFORMS</p>\n          <h2>Learn. Diagnose. Interpret.</h2>\n          <p>\n            Cutline is being built as a connected ecosystem. Education creates the foundation. Diagnostic tools increase visibility. Intelligence products help users understand the larger pattern.\n          </p>',
            '<p class="eyebrow">APPLIED READINESS CONTINUUM (ARC)</p>\n          <h2>Learn. Diagnose. Interpret.</h2>\n          <p>\n            ARC is Cutline\'s named readiness architecture: build the foundation through education, surface system-pattern visibility through CRD, and move toward leadership interpretation through LIB. Cutline Academy delivers the education layer, while Cutline Intelligence provides adjacent public-source research and context.\n          </p>',
        ),
    ],
    ROOT / "services.html": [
        (
            '<p class="eyebrow">HOW THE SYSTEM FITS TOGETHER</p>\n          <h2>Each product has a different job.</h2>\n          <p>Cutline is intentionally not one giant consulting package. Different products solve different problems and carry different evidence and eligibility requirements.</p>',
            '<p class="eyebrow">APPLIED READINESS CONTINUUM (ARC)</p>\n          <h2>One readiness architecture. Different products do different jobs.</h2>\n          <p>ARC organizes Cutline\'s readiness progression from foundational learning to diagnostic visibility and future leadership interpretation. Cutline Academy is the delivery platform; CRF, CRD, and LIB are distinct layers with their own evidence, eligibility, and use boundaries.</p>',
        ),
        (
            '<div><strong>1. Academy</strong><span>Build capability through structured education.</span></div>\n          <div><strong>2. CRF</strong><span>Establish the readiness and systems-thinking foundation.</span></div>\n          <div><strong>3. CRD</strong><span>Surface structured system-pattern signals through a controlled diagnostic.</span></div>\n          <div><strong>4. LIB</strong><span>Future leadership interpretation for eligible evidence and use cases.</span></div>',
            '<div><strong>Platform — Academy</strong><span>Deliver structured professional education and learner progression.</span></div>\n          <div><strong>1. Learn — CRF</strong><span>Establish the readiness and systems-thinking foundation.</span></div>\n          <div><strong>2. Diagnose — CRD</strong><span>Surface structured system-pattern signals through a controlled diagnostic.</span></div>\n          <div><strong>3. Interpret — LIB</strong><span>Provide future leadership interpretation for eligible evidence and use cases.</span></div>',
        ),
    ],
}

changed = []
for path, pairs in replacements.items():
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"{path.name}: expected one guarded ARC replacement, found {count}")
        text = text.replace(old, new, 1)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(path.name)

print("ARC positioning updated:")
for item in changed:
    print(f" - {item}")
