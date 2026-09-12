#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one guarded replacement, found {count}\nTARGET: {old[:180]}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# ---------------------------------------------------------------------------
# Homepage: restore the correct hierarchy.
# Academy is the delivery platform. ARC layers are CRF -> CRD -> LIB.
# ---------------------------------------------------------------------------
replace_once(
    "index.html",
    """          <p>\n            ARC is Cutline's named readiness architecture: build the foundation through education, surface system-pattern visibility through CRD, and move toward leadership interpretation through LIB. Cutline Academy delivers the education layer, while Cutline Intelligence provides adjacent public-source research and context.\n          </p>""",
    """          <p>\n            The Applied Readiness Continuum (ARC) is Cutline's named readiness architecture. Cutline Academy is the delivery platform. Compliance Readiness Fundamentals (CRF) builds the foundation, the Compliance Readiness Diagnostic (CRD) creates structured system-pattern visibility, and the Leadership Intelligence Brief (LIB) is the planned interpretation layer. Cutline Intelligence provides adjacent public-source research and context.\n          </p>""",
)

old_home_cards = """        <div class=\"product-grid\">\n          <article class=\"product-card active-product featured-product\">\n            <div class=\"product-top\"><span class=\"product-step\">Education Platform</span><span class=\"status-pill pending\">Active Build</span></div>\n            <h3>Cutline Academy</h3>\n            <p class=\"product-subtitle\">The owned professional-education platform for Cutline programs.</p>\n            <p>\n              Cutline Academy is the delivery system for structured training, learner progression, assessment, completion, certificate identification, and future program expansion.\n            </p>\n            <ul class=\"clean-list\">\n              <li>Initial flagship: Compliance Readiness Fundamentals v3.0</li>\n              <li>Built for repeatable professional education</li>\n              <li>Designed to support future specialized master-class programs</li>\n              <li>Separate from consulting and regulatory representation</li>\n            </ul>\n            <a class=\"btn btn-primary\" href=\"learning-hub.html#academy\">Explore Cutline Academy</a>\n          </article>\n\n          <article id=\"crd\" class=\"product-card active-product\">"""

new_home_cards = """        <div class=\"academy-platform-strip\">\n          <div>\n            <p class=\"eyebrow\">DELIVERY PLATFORM</p>\n            <h3>Cutline Academy</h3>\n            <p>The Academy delivers Cutline's structured education and future specialized capability programs. It supports the readiness architecture; it is not itself one of the three ARC layers.</p>\n          </div>\n          <a class=\"btn btn-ghost\" href=\"learning-hub.html#academy\">Explore Cutline Academy</a>\n        </div>\n\n        <div class=\"product-grid\">\n          <article class=\"product-card active-product featured-product\">\n            <div class=\"product-top\"><span class=\"product-step\">1 · Learn</span><span class=\"status-pill pending\">Preparing for Delivery</span></div>\n            <h3>Compliance Readiness Fundamentals (CRF)</h3>\n            <p class=\"product-subtitle\">The systems-thinking foundation for the Applied Readiness Continuum.</p>\n            <p>Compliance Readiness Fundamentals teaches the common language behind People, Processes, Product, decision authority, verification, documentation, and operating pressure before learners move into diagnostic or interpretation layers.</p>\n            <a class=\"btn btn-primary\" href=\"learning-hub.html#fundamentals\">Explore Fundamentals</a>\n          </article>\n\n          <article id=\"crd\" class=\"product-card active-product\">"""
replace_once("index.html", old_home_cards, new_home_cards)

replace_once(
    "index.html",
    '<div class="product-top"><span class="product-step">Product — Diagnose</span><span class="status-pill pending">Live Pilot</span></div>',
    '<div class="product-top"><span class="product-step">2 · Diagnose</span><span class="status-pill pending">Live Pilot</span></div>',
)
replace_once(
    "index.html",
    '<div class="product-top"><span class="product-step">Product — Interpret</span><span class="status-pill pending">Future Layer</span></div>',
    '<div class="product-top"><span class="product-step">3 · Interpret</span><span class="status-pill pending">Future Layer</span></div>',
)

# Introduce USDA-FSIS once in visible homepage copy before later shorthand.
replace_once(
    "index.html",
    "facility-specific regulatory consulting for establishments currently regulated by USDA-FSIS is outside scope.",
    "facility-specific regulatory consulting for establishments currently regulated by the U.S. Department of Agriculture Food Safety and Inspection Service (USDA-FSIS) is outside scope.",
)

# ---------------------------------------------------------------------------
# Products page: remove acronym-first navigation/copy and align architecture.
# ---------------------------------------------------------------------------
replace_once("services.html", '<a href="#crd">CRD Pilot</a>', '<a href="#crd">Diagnostic Pilot</a>')
replace_once("services.html", '<a href="#lib">LIB</a>', '<a href="#lib">Leadership Brief</a>')
replace_once(
    "services.html",
    "Cutline's product architecture is designed as a connected readiness system: professional education through Cutline Academy, diagnostic visibility through CRD, and deeper leadership interpretation through future intelligence products.",
    "Cutline's product architecture is designed as a connected readiness system: professional education through Cutline Academy, diagnostic visibility through the Compliance Readiness Diagnostic (CRD), and deeper leadership interpretation through the planned Leadership Intelligence Brief (LIB).",
)
replace_once("services.html", '>View CRD Pilot<', '>View Diagnostic Pilot<')
replace_once("services.html", '<h3>Compliance Readiness Fundamentals</h3>', '<h3>Compliance Readiness Fundamentals (CRF)</h3>')
replace_once("services.html", '<h2>Compliance Readiness Diagnostic</h2>', '<h2>Compliance Readiness Diagnostic (CRD)</h2>')
replace_once("services.html", '<h2>Leadership Intelligence Brief</h2>', '<h2>Leadership Intelligence Brief (LIB)</h2>')

# ---------------------------------------------------------------------------
# Academy: introduce acronyms before shorthand and keep diagnostic separate.
# ---------------------------------------------------------------------------
replace_once("learning-hub.html", '<a href="services.html#crd">CRD Pilot</a>', '<a href="services.html#crd">Diagnostic Pilot</a>')
replace_once("learning-hub.html", '<h2>Compliance Readiness Fundamentals</h2>', '<h2>Compliance Readiness Fundamentals (CRF)</h2>')
replace_once(
    "learning-hub.html",
    "Cutline Academy builds capability. CRD provides structured diagnostic visibility. LIB is planned as a future leadership interpretation layer. Cutline Intelligence develops independent public-source analysis. Together, these products support the larger goal of stronger food safety thinking and organizational readiness.",
    "Cutline Academy builds capability. The Compliance Readiness Diagnostic (CRD) provides structured diagnostic visibility. The Leadership Intelligence Brief (LIB) is planned as a future leadership interpretation layer. Cutline Intelligence develops independent public-source analysis. Together, these products support the larger goal of stronger food safety thinking and organizational readiness.",
)
replace_once(
    "learning-hub.html",
    "establishments currently regulated by USDA-FSIS.",
    "establishments currently regulated by the U.S. Department of Agriculture Food Safety and Inspection Service (USDA-FSIS).",
)

# ---------------------------------------------------------------------------
# Ethics: do not lead with unexplained diagnostic shorthand.
# ---------------------------------------------------------------------------
replace_once("ethics.html", '<a href="#crd-boundaries">CRD Boundaries</a>', '<a href="#crd-boundaries">Diagnostic Boundaries</a>')
replace_once(
    "ethics.html",
    '<div class="card"><h3>Compliance Readiness Diagnostic</h3><p>System-pattern visibility for eligible internal readiness discussion. CRD is not a compliance score, regulatory finding, or corrective-action service.</p></div>',
    '<div class="card"><h3>Compliance Readiness Diagnostic (CRD)</h3><p>System-pattern visibility for eligible internal readiness discussion. CRD is not a compliance score, regulatory finding, or corrective-action service.</p></div>',
)
replace_once(
    "ethics.html",
    "Facility-specific regulatory consulting is not available to establishments currently regulated by USDA-FSIS.",
    "Facility-specific regulatory consulting is not available to establishments currently regulated by the U.S. Department of Agriculture Food Safety and Inspection Service (USDA-FSIS).",
)

# ---------------------------------------------------------------------------
# YouTube: introduce the diagnostic before using CRD shorthand.
# ---------------------------------------------------------------------------
replace_once(
    "youtube.html",
    "The channel will support the same product ecosystem: Compliance Readiness Fundamentals, the CRD live pilot, and future system-pattern interpretation content.",
    "The channel will support the same product ecosystem: Compliance Readiness Fundamentals, the Compliance Readiness Diagnostic (CRD) live pilot, and future system-pattern interpretation content.",
)

# ---------------------------------------------------------------------------
# Shared JS: restore a sitewide paper promo, not a CRD promo.
# ---------------------------------------------------------------------------
site_js = ROOT / "site.js"
text = site_js.read_text(encoding="utf-8")
anchor = "  const GA_DISABLE_KEY = `ga-disable-${GA_ID}`;\n"
if "PAPER_PROMO_SESSION_KEY" not in text:
    if text.count(anchor) != 1:
        raise SystemExit("site.js: promo constant anchor missing")
    text = text.replace(anchor, anchor + "  const PAPER_PROMO_SESSION_KEY = 'cutline_paper_promo_seen_v1';\n", 1)

function_anchor = "  function initFooterPrivacyControl() {\n"
promo_function = r'''  function initPaperPromo() {
    const path = window.location.pathname;
    const excluded = [
      '/intelligence/producer-direct-interstate-meat-commerce/',
      '/privacy.html',
      '/terms.html',
      '/accessibility.html',
      '/404.html'
    ];
    if (excluded.some((item) => path === item || path.endsWith(item))) return;

    try {
      if (sessionStorage.getItem(PAPER_PROMO_SESSION_KEY) === '1') return;
    } catch (_) {}

    let opened = false;
    let retryCount = 0;

    const remember = () => {
      try { sessionStorage.setItem(PAPER_PROMO_SESSION_KEY, '1'); } catch (_) {}
    };

    const openPromo = () => {
      if (opened || document.querySelector('[data-paper-promo]')) return;
      if (document.querySelector('[data-cutline-consent]') && retryCount < 10) {
        retryCount += 1;
        window.setTimeout(openPromo, 1800);
        return;
      }

      opened = true;
      remember();
      const promo = document.createElement('aside');
      promo.className = 'paper-promo';
      promo.setAttribute('data-paper-promo', '');
      promo.setAttribute('role', 'dialog');
      promo.setAttribute('aria-labelledby', 'paper-promo-title');
      promo.setAttribute('aria-describedby', 'paper-promo-copy');
      promo.innerHTML = `
        <button class="paper-promo__close" type="button" aria-label="Close paper promotion">×</button>
        <p class="eyebrow">NEW CUTLINE INTELLIGENCE PAPER</p>
        <h2 id="paper-promo-title">A Safe Path to Producer-Direct Interstate Meat Commerce</h2>
        <p id="paper-promo-copy">Read Cutline's 50-state analysis of producer access, inspection pathways, market structure, food safety, and a proposed inspected path forward.</p>
        <div class="paper-promo__actions">
          <a class="btn btn-primary" href="/intelligence/producer-direct-interstate-meat-commerce/">Read the analysis</a>
          <a class="paper-promo__download" href="/downloads/producer-direct-interstate-meat-commerce-full-report.pdf" download>Download full report</a>
        </div>`;
      document.body.appendChild(promo);
      requestAnimationFrame(() => promo.classList.add('is-visible'));
      track('paper_promo_view', { page_path: window.location.pathname });

      const close = () => {
        promo.classList.remove('is-visible');
        window.setTimeout(() => promo.remove(), 180);
      };
      promo.querySelector('.paper-promo__close')?.addEventListener('click', close);
      promo.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
          track('paper_promo_click', { destination: link.href, page_path: window.location.pathname });
          close();
        });
      });
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && document.body.contains(promo)) close();
      }, { once: true });
    };

    const onScroll = () => {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      if (scrollable > 0 && window.scrollY / scrollable >= 0.30) {
        window.removeEventListener('scroll', onScroll);
        openPromo();
      }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    window.setTimeout(openPromo, 9000);
  }

'''
if "function initPaperPromo()" not in text:
    if text.count(function_anchor) != 1:
        raise SystemExit("site.js: promo function anchor missing")
    text = text.replace(function_anchor, promo_function + function_anchor, 1)

call_anchor = "    initAnalyticsEvents();\n    initFooterPrivacyControl();\n"
if "    initPaperPromo();\n" not in text:
    if text.count(call_anchor) != 1:
        raise SystemExit("site.js: promo call anchor missing")
    text = text.replace(call_anchor, "    initAnalyticsEvents();\n    initPaperPromo();\n    initFooterPrivacyControl();\n", 1)
site_js.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Styling for the platform strip + paper promo.
# ---------------------------------------------------------------------------
css = ROOT / "enhancements.css"
text = css.read_text(encoding="utf-8")
css_marker = "\n@media (max-width:760px){\n"
css_block = r'''

.academy-platform-strip{
  display:grid;
  grid-template-columns:minmax(0,1fr) auto;
  gap:1.5rem;
  align-items:center;
  margin:0 0 1.5rem;
  padding:1.35rem 1.5rem;
  border:1px solid rgba(255,255,255,.10);
  border-left:4px solid var(--red-text);
  border-radius:16px;
  background:linear-gradient(120deg,rgba(255,255,255,.045),rgba(255,255,255,.018));
}
.academy-platform-strip h3{margin:.1rem 0 .35rem;color:#fff;font-size:1.35rem}
.academy-platform-strip p{margin:.2rem 0;color:#c2c9d4}
.academy-platform-strip .eyebrow{color:var(--red-text);margin-bottom:.25rem}

.paper-promo{
  position:fixed;
  right:1.2rem;
  bottom:1.2rem;
  z-index:360;
  width:min(430px,calc(100vw - 2rem));
  padding:1.35rem;
  border:1px solid rgba(255,255,255,.14);
  border-top:3px solid var(--red-text);
  border-radius:18px;
  background:linear-gradient(155deg,rgba(13,18,28,.99),rgba(4,9,17,.99));
  box-shadow:0 24px 70px rgba(0,0,0,.58);
  opacity:0;
  transform:translateY(16px);
  pointer-events:none;
  transition:opacity .18s ease,transform .18s ease;
}
.paper-promo.is-visible{opacity:1;transform:translateY(0);pointer-events:auto}
.paper-promo__close{
  position:absolute;
  top:.65rem;
  right:.75rem;
  display:grid;
  place-items:center;
  width:36px;
  height:36px;
  border:1px solid rgba(255,255,255,.12);
  border-radius:999px;
  background:rgba(255,255,255,.035);
  color:#fff;
  font-size:1.35rem;
  line-height:1;
  cursor:pointer;
}
.paper-promo__close:hover,.paper-promo__close:focus-visible{border-color:var(--red-text);color:var(--red-text)}
.paper-promo .eyebrow{padding-right:2.4rem;margin-bottom:.45rem;color:var(--red-text)}
.paper-promo h2{margin:0 2.2rem .65rem 0;color:#fff;font-size:1.3rem;line-height:1.15}
.paper-promo p:not(.eyebrow){margin:0;color:#c4ccd7;line-height:1.55}
.paper-promo__actions{display:flex;flex-wrap:wrap;gap:.85rem;align-items:center;margin-top:1rem}
.paper-promo__download{color:#fff;font-weight:800;text-decoration:none}
.paper-promo__download:hover,.paper-promo__download:focus-visible{color:var(--red-text)}
'''
if ".paper-promo{" not in text:
    if text.count(css_marker) != 1:
        raise SystemExit("enhancements.css: media marker missing")
    text = text.replace(css_marker, css_block + css_marker, 1)

mobile_old = """@media (max-width:760px){\n  .consent-banner__inner{\n    grid-template-columns:1fr;\n  }"""
mobile_new = """@media (max-width:760px){\n  .academy-platform-strip{grid-template-columns:1fr;align-items:start}\n  .paper-promo{right:.75rem;bottom:.75rem;width:calc(100vw - 1.5rem)}\n  .consent-banner__inner{\n    grid-template-columns:1fr;\n  }"""
if mobile_old in text:
    text = text.replace(mobile_old, mobile_new, 1)
css.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Permanent release rule: product acronyms must be defined before shorthand.
# ---------------------------------------------------------------------------
validator = ROOT / "tools" / "validate_site.py"
text = validator.read_text(encoding="utf-8")
const_anchor = "LEGAL_LINKS = (\"/privacy.html\", \"/terms.html\", \"/accessibility.html\")\n"
const_insert = '''LEGAL_LINKS = ("/privacy.html", "/terms.html", "/accessibility.html")
PRODUCT_ACRONYMS = {
    "ARC": "Applied Readiness Continuum (ARC)",
    "CRF": "Compliance Readiness Fundamentals (CRF)",
    "CRD": "Compliance Readiness Diagnostic (CRD)",
    "LIB": "Leadership Intelligence Brief (LIB)",
}
'''
if "PRODUCT_ACRONYMS = {" not in text:
    if text.count(const_anchor) != 1:
        raise SystemExit("validator: acronym constant anchor missing")
    text = text.replace(const_anchor, const_insert, 1)

validation_anchor = '''        required_positioning = REQUIRED_POSITIONING.get(rel.as_posix(), ())
        for phrase in required_positioning:
            if phrase.lower() not in text.lower():
                errors.append(f"{rel}: required Cutline positioning missing: {phrase}")
'''
validation_insert = validation_anchor + '''
        body_source = text.split("<body", 1)[1] if "<body" in text else text
        for acronym, definition in PRODUCT_ACRONYMS.items():
            match = re.search(rf"\\b{re.escape(acronym)}\\b", body_source)
            if not match:
                continue
            definition_index = body_source.find(definition)
            if definition_index == -1 or definition_index > match.start():
                errors.append(f"{rel}: {acronym} appears before it is introduced as '{definition}'")
'''
if "appears before it is introduced" not in text:
    if validation_anchor not in text:
        raise SystemExit("validator: acronym validation anchor missing")
    text = text.replace(validation_anchor, validation_insert, 1)
validator.write_text(text, encoding="utf-8")

print("Website v2.2 content architecture correction applied.")
