(() => {
  'use strict';

  const GA_ID = 'G-Z4KHLSPY1T';
  const CONSENT_KEY = 'cutline_analytics_consent_v1';

  const gtagSafe = (...args) => {
    if (typeof window.gtag === 'function') window.gtag(...args);
  };

  function applyConsent(value) {
    const granted = value === 'granted';
    gtagSafe('consent', 'update', {
      analytics_storage: granted ? 'granted' : 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
  }

  function buildConsentBanner() {
    if (document.querySelector('[data-cutline-consent]')) return;

    const banner = document.createElement('section');
    banner.className = 'consent-banner';
    banner.setAttribute('data-cutline-consent', '');
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Analytics privacy choice');
    banner.innerHTML = `
      <div class="consent-banner__inner">
        <div>
          <strong>Privacy choice</strong>
          <p>Cutline uses optional Google Analytics to understand site use and improve our products. You can allow analytics or continue with essential site functions only.</p>
        </div>
        <div class="consent-banner__actions">
          <button type="button" class="btn btn-primary" data-consent="granted">Allow analytics</button>
          <button type="button" class="btn btn-ghost" data-consent="denied">Essential only</button>
          <a href="/privacy.html">Privacy</a>
        </div>
      </div>`;

    document.body.appendChild(banner);

    banner.querySelectorAll('[data-consent]').forEach((button) => {
      button.addEventListener('click', () => {
        const value = button.getAttribute('data-consent');
        localStorage.setItem(CONSENT_KEY, value);
        applyConsent(value);
        banner.remove();
      });
    });
  }

  function initConsent() {
    const saved = localStorage.getItem(CONSENT_KEY);
    if (saved === 'granted' || saved === 'denied') {
      applyConsent(saved);
      return;
    }
    buildConsentBanner();
  }

  function initNavigation() {
    const btn = document.querySelector('.menu-toggle');
    const nav = document.getElementById('site-nav');
    if (!btn || !nav) return;

    const closeMenu = () => {
      nav.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      btn.setAttribute('aria-label', 'Open menu');
    };

    btn.addEventListener('click', () => {
      const isOpen = btn.getAttribute('aria-expanded') === 'true';
      if (isOpen) {
        closeMenu();
      } else {
        nav.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
        btn.setAttribute('aria-label', 'Close menu');
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeMenu();
    });

    nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  }

  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener('click', (event) => {
        const href = link.getAttribute('href');
        if (!href || href === '#') return;
        const target = document.querySelector(href);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  function classifyLink(link) {
    const href = link.getAttribute('href') || '';
    if (!href) return null;
    if (href.startsWith('mailto:')) return 'contact_email_click';
    if (href.includes('crd.cutlinecompliance.com')) return 'crd_portal_click';
    if (href.includes('learning-hub.html') || href.startsWith('/academy')) return 'academy_click';
    if (href.includes('/intelligence/')) return 'intelligence_click';
    if (href.toLowerCase().endsWith('.pdf') || link.hasAttribute('download')) return 'asset_download';
    if (href.includes('youtube.com')) return 'youtube_click';
    if (href.includes('linkedin.com')) return 'linkedin_click';
    return null;
  }

  function initAnalyticsEvents() {
    document.addEventListener('click', (event) => {
      const link = event.target.closest('a');
      if (!link) return;
      const eventName = classifyLink(link);
      if (!eventName) return;
      gtagSafe('event', eventName, {
        link_text: (link.textContent || '').trim().slice(0, 120),
        link_url: link.href || '',
        page_path: window.location.pathname
      });
    });
  }

  function initFooterLinks() {
    const footer = document.querySelector('.footer');
    if (!footer || footer.querySelector('.legal-footer-links')) return;

    const wrap = document.createElement('div');
    wrap.className = 'container legal-footer-links';
    wrap.innerHTML = `
      <a href="/privacy.html">Privacy</a>
      <a href="/terms.html">Terms of Use</a>
      <a href="/accessibility.html">Accessibility</a>`;
    footer.appendChild(wrap);
  }

  function initYear() {
    document.querySelectorAll('#yr,[data-current-year]').forEach((el) => {
      el.textContent = String(new Date().getFullYear());
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initYear();
    initNavigation();
    initSmoothAnchors();
    initConsent();
    initAnalyticsEvents();
    initFooterLinks();
  });
})();
