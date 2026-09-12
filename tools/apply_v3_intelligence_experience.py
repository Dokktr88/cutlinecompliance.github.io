#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
VALIDATOR = ROOT / "tools" / "validate_site.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one target, found {count}")
    return text.replace(old, new, 1)


index = INDEX.read_text(encoding="utf-8")

index = replace_once(
    index,
    '  <link rel="stylesheet" href="/enhancements.css?v=2" />',
    '  <link rel="stylesheet" href="/enhancements.css?v=2" />\n  <link rel="stylesheet" href="/v3.css?v=1" />',
    "v3 stylesheet",
)

index = replace_once(
    index,
    '<body id="top">',
    '<body id="top" data-site-version="3.0">',
    "site version marker",
)

old_hero_panel = '''        <aside class="hero-panel" aria-label="Cutline system framework">
          <img src="cutline-logo.png" alt="Cutline Compliance — People. Processes. Product." class="hero-logo" width="600" height="188" loading="eager" decoding="async" />

          <div class="brand-statement">
            <p><strong>Understand the system.</strong></p>
            <p><strong>Diagnose the gaps.</strong></p>
            <p><strong>Interpret the pattern.</strong></p>
          </div>

          <div class="signal-grid">
            <div><span>People</span><p>Knowledge, responsibility, authority, communication, and decision clarity.</p></div>
            <div><span>Processes</span><p>Workflow, verification, documentation, feedback, and control.</p></div>
            <div><span>Product</span><p>Protection created by systems that perform consistently in the real world.</p></div>
          </div>
        </aside>'''

new_hero_panel = '''        <aside class="hero-panel intelligence-map-panel" aria-label="Cutline signal intelligence model">
          <div class="v3-map-header">
            <span class="v3-map-kicker">CUTLINE SIGNAL MAP</span>
            <span class="v3-map-status">Conceptual system model</span>
          </div>

          <svg class="cutline-signal-map" viewBox="0 0 720 520" role="img" aria-labelledby="signal-map-title signal-map-desc">
            <title id="signal-map-title">Cutline signal-to-intelligence model</title>
            <desc id="signal-map-desc">A conceptual diagram showing People, Processes, and Product signals converging into patterns, crossing the Cutline interpretation boundary, and becoming decision-relevant intelligence.</desc>

            <text x="36" y="39" class="map-micro" font-size="11">SYSTEM SIGNALS</text>
            <text x="282" y="39" class="map-micro" font-size="11">PATTERN LAYER</text>
            <text x="548" y="39" class="map-micro" font-size="11">INTERPRETATION</text>

            <path d="M190 126 C250 126 260 220 324 220" class="signal-path path-delay-1" />
            <path d="M190 252 C250 252 270 236 324 236" class="signal-path path-delay-2" />
            <path d="M190 378 C250 378 260 252 324 252" class="signal-path path-delay-3" />
            <path d="M438 236 C480 236 500 236 532 236" class="signal-path accent path-delay-4" />

            <circle cx="220" cy="126" r="4.5" class="signal-dot dot-delay-1" />
            <circle cx="239" cy="183" r="4" class="signal-dot red dot-delay-2" />
            <circle cx="234" cy="252" r="4.5" class="signal-dot dot-delay-2" />
            <circle cx="245" cy="317" r="4" class="signal-dot red dot-delay-3" />
            <circle cx="220" cy="378" r="4.5" class="signal-dot dot-delay-3" />
            <circle cx="478" cy="236" r="5" class="signal-dot red dot-delay-4" />

            <rect x="35" y="82" width="155" height="87" rx="14" class="map-node" />
            <text x="57" y="116" class="map-label" font-size="18">People</text>
            <text x="57" y="139" class="map-micro" font-size="10">AUTHORITY · KNOWLEDGE</text>
            <text x="57" y="155" class="map-micro" font-size="10">COMMUNICATION</text>

            <rect x="35" y="208" width="155" height="87" rx="14" class="map-node" />
            <text x="57" y="242" class="map-label" font-size="18">Processes</text>
            <text x="57" y="265" class="map-micro" font-size="10">WORKFLOW · VERIFICATION</text>
            <text x="57" y="281" class="map-micro" font-size="10">DOCUMENTATION</text>

            <rect x="35" y="334" width="155" height="87" rx="14" class="map-node" />
            <text x="57" y="368" class="map-label" font-size="18">Product</text>
            <text x="57" y="391" class="map-micro" font-size="10">PROTECTION · CONTROL</text>
            <text x="57" y="407" class="map-micro" font-size="10">REAL-WORLD PERFORMANCE</text>

            <rect x="324" y="181" width="114" height="110" rx="16" class="map-node-accent" />
            <text x="381" y="215" text-anchor="middle" class="map-micro" font-size="10">SIGNAL</text>
            <text x="381" y="237" text-anchor="middle" class="map-label" font-size="15">Pattern</text>
            <text x="381" y="257" text-anchor="middle" class="map-label" font-size="15">Convergence</text>
            <text x="381" y="278" text-anchor="middle" class="map-micro" font-size="9">RELATIONSHIPS · PRESSURE</text>

            <line x1="496" y1="78" x2="496" y2="425" class="cutline-divider" />
            <text x="508" y="411" class="cutline-label" transform="rotate(-90 508 411)">THE CUTLINE</text>

            <rect x="532" y="177" width="154" height="118" rx="16" class="map-node-intelligence" />
            <text x="609" y="209" text-anchor="middle" class="map-micro map-dark-label" font-size="9">DECISION-RELEVANT</text>
            <text x="609" y="236" text-anchor="middle" class="map-dark-label" font-size="17" font-family="Aptos,Arial,Helvetica,sans-serif" font-weight="900">Intelligence</text>
            <text x="609" y="259" text-anchor="middle" class="map-micro map-dark-label" font-size="9">EVIDENCE</text>
            <text x="609" y="276" text-anchor="middle" class="map-micro map-dark-label" font-size="9">INTERPRETATION</text>

            <text x="325" y="466" class="map-micro" font-size="10">OBSERVE → CONNECT → INTERPRET</text>
          </svg>

          <p class="v3-map-note">Conceptual model only — not a live operational feed. It illustrates how Cutline separates observable signals from interpretation and decision-relevant context.</p>
        </aside>'''

index = replace_once(index, old_hero_panel, new_hero_panel, "hero signal map")

current_intelligence = '''    <section class="v3-intelligence-feature" aria-labelledby="v3-current-intelligence">
      <div class="container">
        <div class="v3-intelligence-label"><span>01</span> Current Intelligence</div>

        <div class="v3-intelligence-grid">
          <article class="v3-publication-spotlight">
            <div class="v3-publication-content">
              <p class="v3-publication-kicker">Published Analysis · Food Systems & Market Structure</p>
              <h2 id="v3-current-intelligence">A Safe Path to Producer-Direct Interstate Meat Commerce</h2>
              <p class="v3-publication-summary">A 50-state public-source analysis examining producer access, inspection pathways, market structure, food safety, statutory barriers, and a proposed inspected path forward.</p>
              <div class="v3-evidence-tags" aria-label="Analysis characteristics">
                <span>50-state analysis</span>
                <span>Public-source evidence</span>
                <span>Policy + market structure</span>
              </div>
            </div>

            <div class="v3-publication-actions">
              <a class="btn btn-primary" href="intelligence/producer-direct-interstate-meat-commerce/">Read the analysis</a>
              <a class="v3-publication-download" href="downloads/producer-direct-interstate-meat-commerce-full-report.pdf">Download full report</a>
            </div>
          </article>

          <aside class="v3-intelligence-method" aria-label="How Cutline develops intelligence">
            <p class="eyebrow">HOW CUTLINE WORKS</p>
            <h2>From signal to usable intelligence.</h2>

            <div class="v3-method-step">
              <span>01</span>
              <div><strong>Observe</strong><p>Start with information that can be documented and checked.</p></div>
            </div>
            <div class="v3-method-step">
              <span>02</span>
              <div><strong>Connect</strong><p>Look for relationships, convergence, pressure, and competing explanations.</p></div>
            </div>
            <div class="v3-method-step">
              <span>03</span>
              <div><strong>Interpret</strong><p>Translate the pattern into useful context without overstating certainty.</p></div>
            </div>

            <p class="v3-method-note">Evidence and interpretation remain visibly separate. The visual system communicates analytical method — not simulated real-time monitoring.</p>
          </aside>
        </div>
      </div>
    </section>

'''

index = replace_once(
    index,
    '    <section class="cred-strip-section" aria-label="Cutline capabilities">',
    current_intelligence + '    <section class="cred-strip-section" aria-label="Cutline capabilities">',
    "current intelligence module",
)

old_later_card = '''        <aside class="intelligence-card">
          <h3>Current flagship analysis</h3>
          <p><strong>A Safe Path to Producer-Direct Interstate Meat Commerce</strong></p>
          <p>A 50-state policy, food-safety, market-structure, and intelligence analysis examining current pathways, statutory barriers, and a proposed inspected approach to broader producer access.</p>
          <a class="link-inline" href="intelligence/producer-direct-interstate-meat-commerce/">Read the analysis →</a>
        </aside>'''

new_later_card = '''        <aside class="intelligence-card">
          <h3>Intelligence standard</h3>
          <div class="v3-intelligence-standard">
            <div class="v3-standard-row"><span class="v3-standard-dot"></span><div><strong>Evidence first</strong><p>Document what is verifiable before moving to interpretation.</p></div></div>
            <div class="v3-standard-row"><span class="v3-standard-dot"></span><div><strong>Alternatives visible</strong><p>Consider competing explanations rather than forcing one narrative.</p></div></div>
            <div class="v3-standard-row"><span class="v3-standard-dot"></span><div><strong>Confidence matched to evidence</strong><p>Make the reasoning visible and avoid certainty the sources cannot support.</p></div></div>
          </div>
          <a class="link-inline" href="intelligence/">Explore Cutline Intelligence →</a>
        </aside>'''

index = replace_once(index, old_later_card, new_later_card, "later intelligence standard card")

INDEX.write_text(index, encoding="utf-8")

validator = VALIDATOR.read_text(encoding="utf-8")

validator = replace_once(
    validator,
    '    "index.html": ("Applied Readiness Continuum (ARC)", "Learn. Diagnose. Interpret."),',
    '    "index.html": ("Applied Readiness Continuum (ARC)", "Learn. Diagnose. Interpret.", "CUTLINE SIGNAL MAP", "Current Intelligence", "From signal to usable intelligence."),',
    "validator v3 positioning",
)

needle = '''        if "/site.js?v=1" not in text:
            errors.append(f"{rel}: missing shared site.js")'''
replacement = '''        if "/site.js?v=1" not in text:
            errors.append(f"{rel}: missing shared site.js")
        if rel.as_posix() == "index.html":
            if "/v3.css?v=1" not in text:
                errors.append(f"{rel}: missing Website v3 intelligence stylesheet")
            if 'data-site-version="3.0"' not in text:
                errors.append(f"{rel}: missing Website v3 release marker")
            if "Conceptual model only — not a live operational feed." not in text:
                errors.append(f"{rel}: signal map must retain the non-live-data disclosure")'''
validator = replace_once(validator, needle, replacement, "validator v3 release checks")

VALIDATOR.write_text(validator, encoding="utf-8")
print("Applied Website v3 intelligence experience patch.")
