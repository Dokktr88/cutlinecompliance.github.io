// sw.js — Cutline Compliance
// Network-first for pages so the site does not get stuck on old HTML.
// Cache-first for same-origin static assets after first load.

const CACHE_VERSION = "cutline-v22";
const STATIC_CACHE = `${CACHE_VERSION}-static`;

const STATIC_ASSETS = [
  "/",
  "/index.html",
  "/services.html",
  "/learning-hub.html",
  "/ethics.html",
  "/youtube.html",
  "/styles.css",

  "/cutline-logo.png",
  "/cutline-logo-light-header-600x188.png",
  "/cutline-app-icon-192x192.png",
  "/cutline-app-icon-512x512.png",
  "/cutline-apple-touch-icon-180x180.png",
  "/cutline-favicon-16x16.png",
  "/cutline-favicon-32x32.png",
  "/cutline-profile-icon-1024x1024.png",
  "/CRD_customer.png",
  "/favicon.ico"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) =>
      Promise.allSettled(STATIC_ASSETS.map((asset) => cache.add(asset)))
    )
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => !key.startsWith(CACHE_VERSION))
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;

  if (req.method !== "GET") return;

  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;

  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(STATIC_CACHE).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() =>
          caches.match(req).then((cached) => cached || caches.match("/index.html"))
        )
    );
    return;
  }

  if (sameOrigin) {
    event.respondWith(
      caches.match(req).then((cached) => {
        if (cached) return cached;

        return fetch(req)
          .then((res) => {
            const copy = res.clone();
            caches.open(STATIC_CACHE).then((cache) => cache.put(req, copy));
            return res;
          })
          .catch(() => cached);
      })
    );
  }
});
