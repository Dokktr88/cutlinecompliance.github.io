const CACHE = "cutline-v4";
const ASSETS = [
  "/",
  "/index.html",
  "/styles.css",
  "/youtube.html",
  "/manifest.webmanifest",
  "/cutline-open-512.png",
  "/favicon-32.png",
  "/favicon.ico",
  "/Cutline_text_1.png",
  "/Cutline_text_2.png",
  "/Blue Shirt White Background3v3.jpg",
  "/IMG_9489.PNG",
  "/IMG_9490.PNG",
  "/IMG_9491.PNG",
  "/IMG_9492.PNG",
  "/IMG_9499.PNG"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then((r) => r || fetch(e.request))
  );
});
