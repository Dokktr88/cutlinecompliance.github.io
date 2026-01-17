const CACHE = "cutline-v2";

const ASSETS = [
  "/",
  "/index.html",
  "/styles.css",
  "/manifest.webmanifest",
  "/youtube.html",
  "/cutline-open-512.png",
  "/favicon-32.png",
  "/favicon.ico",
  "/IMG_9490.PNG",
  "/IMG_9491.PNG",
  "/IMG_9492.PNG",
  "/IMG_9499.PNG",
  "/IMG_9489.PNG"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll(ASSETS))
      .catch(() => {})
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then((r) => r || fetch(e.request))
  );
});
