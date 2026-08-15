const CACHE_NAME = "tech-intel-v3";
// Scope-derived prefix — works for both /tech-blog/ and /tech-blog-en/
// (registration scope always ends with "/")
const SCOPE = self.registration.scope;
const SCOPE_PATH = new URL(SCOPE).pathname; // e.g. "/tech-blog/"
const STATIC_ASSETS = ["css/", "js/", "fonts/", "images/icon-"];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then((c) => c.addAll([
        SCOPE,                                   // homepage (HTML core shell)
        SCOPE + "css/bbc.css?v=9",
        SCOPE + "css/news-ticker.css?v=2",
        SCOPE + "css/header.css?v=1",
        SCOPE + "manifest.json",
        SCOPE + "fonts/Bornomala-Regular.woff2",
        SCOPE + "fonts/Bornomala-Bold.woff2",
        SCOPE + "fonts/roboto-latin-var.woff2",
        SCOPE + "js/busuanzi.pure.mini.js",
      ]))
      .catch(() => {})                           // any single failure must not break install
  );
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  const isStatic = STATIC_ASSETS.some((p) => url.pathname.startsWith(SCOPE_PATH + p));
  if (isStatic) {
    // cache-first + background fill (previous logic, now with correct prefix)
    e.respondWith(
      caches.open(CACHE_NAME).then((c) =>
        c.match(e.request).then((r) =>
          r || fetch(e.request).then((resp) => {
            if (resp.ok) c.put(e.request, resp.clone());
            return resp;
          }).catch(() => r)
        )
      )
    );
  } else {
    // HTML/images: network-first + cache fallback (as before)
    e.respondWith(
      fetch(e.request)
        .then((resp) => {
          if (resp.ok && resp.type === "basic") {
            const clone = resp.clone();
            caches.open(CACHE_NAME).then((c) => c.put(e.request, clone));
          }
          return resp;
        })
        .catch(() => caches.match(e.request))
    );
  }
});
