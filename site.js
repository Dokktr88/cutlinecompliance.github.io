(() => {
  'use strict';

  const GA_ID = 'G-Z4KHLSPY1T';
  const CONSENT_KEY = 'cutline_analytics_consent_v1';
  const GA_DISABLE_KEY = `ga-disable-${GA_ID}`;
  let analyticsLoading = false;

  function getConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (_) { return null; }
  }

  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); return true; } catch (_) { return false; }
  }

  function clearConsent() {
    try { localStorage.removeItem(CONSENT_KEY); } catch (_) {}
  }

  function setAnalyticsEnabled(enabled) {
    window[GA_DISABLE_KEY] = !enabled;
  }

  function ensureGtag() {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag(){ window.dataLayer.push(arguments); };
  }

  function loadAnalytics() {
    if (getConsent() !== 'granted') return;
    setAnalyticsEnabled(true);
    if (window.__cutlineAnalyticsLoaded || analyticsLoading) return;

    analyticsLoading = true;
    ensureGtag();
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);

    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_ID)}`;
    script.onload = () => {
      analyticsLoading = false;
      window.__cutlineAnalyticsLoaded = true;
    };
    script.onerror = () => { analyticsLoading = false; };
    document.head.appendChild(script);
  }

  function track(eventName, params = {}) {
    if (getConsent() !== 'granted') return;
    ensureGtag();
    window.gtag('event', eventName, params);
  }

  function buildConsentBanner() {
    if (document.querySelector('[data-cutline-consent]')) return;

    const banner = document.createElement('section');
    banner.className = 'consent-banner';
    banner.setAttribute('data-cutline-consent', '');
    banner.setAttribute('role', 'region');
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
        setConsent(value);
        if (value === 'granted') {
          setAnalyticsEnabled(true);
          loadAnalytics();
        } else {
          setAnalyticsEnabled(false);
        }
        banner.remove();
      });
    });
  }

  function initConsent() {
    const saved = getConsent();
    if (saved === 'granted') {
      setAnalyticsEnabled(true);
      loadAnalytics();
    } else if (saved === 'denied') {
      setAnalyticsEnabled(false);
    } else {
      setAnalyticsEnabled(false);
      buildConsentBanner();
    }
  }

  function initNavigation() {
    const btn = document.querySelector('.menu-toggle');
    const nav = document.getElementById('site-nav');
    if (!btn || !nav) return;

    const setOpen = (open, returnFocus = false) => {
      nav.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (!open && returnFocus) btn.focus();
    };

    btn.addEventListener('click', () => {
      setOpen(btn.getAttribute('aria-expanded') !== 'true');
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
        setOpen(false, true);
      }
    });

    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setOpen(false));
    });

    setOpen(false);
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
      track(eventName, {
        link_text: (link.textContent || '').trim().slice(0, 120),
        link_url: link.href || '',
        page_path: window.location.pathname
      });
    });
  }

  function initFooterPrivacyControl() {
    const reset = document.querySelector('[data-reset-analytics]');
    if (!reset) return;
    reset.addEventListener('click', () => {
      setAnalyticsEnabled(false);
      clearConsent();
      buildConsentBanner();
    });
  }

  function initYear() {
    document.querySelectorAll('#yr,[data-current-year]').forEach((el) => {
      el.textContent = String(new Date().getFullYear());
    });
  }

  async function retireLegacyServiceWorker() {
    if (!('serviceWorker' in navigator)) return;
    try {
      const registrations = await navigator.serviceWorker.getRegistrations();
      await Promise.all(
        registrations
          .filter((registration) => {
            const active = registration.active || registration.waiting || registration.installing;
            return active && new URL(active.scriptURL).pathname === '/sw.js';
          })
          .map((registration) => registration.unregister())
      );
      if ('caches' in window) {
        const keys = await caches.keys();
        await Promise.all(keys.filter((key) => key.startsWith('cutline-v')).map((key) => caches.delete(key)));
      }
    } catch (_) {
      // Site operation must not depend on cleanup succeeding.
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initYear();
    initNavigation();
    initSmoothAnchors();
    initConsent();
    initAnalyticsEvents();
    initFooterPrivacyControl();
    retireLegacyServiceWorker();
  });
})();
