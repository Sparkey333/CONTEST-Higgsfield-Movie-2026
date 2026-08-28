/* Production Desk — offline cache.
   Everything here is local already, so the only job this does is let the
   installed app keep working after the launcher terminal is closed.

   Bump CACHE when any document changes, otherwise the installed app will
   keep serving the copy it cached on first run. */

const CACHE = "desk-v7";

/* crosswalk.local.js is deliberately absent from this list: it is gitignored,
   may not exist, and a single 404 fails the whole addAll(). */
const ASSETS = [
  "./",
  "./index.html",
  "./director-bible.html",
  "./production-sheet.html",
  "./lookbook-audit.html",
  "./app.webmanifest",
  "./icon.svg",
  "./workflow-sheets.pdf"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      /* individual puts, so one missing file cannot sink the install */
      .then((c) => Promise.all(ASSETS.map((u) => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  /* Documents go NETWORK FIRST. The old cache-first strategy meant the first
     load after replacing the folder showed the previous version of a page —
     which read as "my update didn't happen". Offline still works: the cache
     is the fallback, not the source. */
  const isDoc = req.mode === "navigate" ||
                url.pathname.endsWith(".html") || url.pathname.endsWith("/");
  if (isDoc) {
    e.respondWith(
      fetch(req).then((res) => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() =>
        caches.match(req).then((hit) => hit || caches.match("./index.html"))
      )
    );
    return;
  }

  /* Everything else (icon, manifest, the PDF) stays cache first with a
     background refresh — those change rarely and load instantly this way. */
  e.respondWith(
    caches.match(req).then((hit) => {
      if (hit) {
        fetch(req).then((res) => {
          if (res && res.ok) caches.open(CACHE).then((c) => c.put(req, res));
        }).catch(() => {});
        return hit;
      }
      return fetch(req).then((res) => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() => caches.match("./index.html"));
    })
  );
});
