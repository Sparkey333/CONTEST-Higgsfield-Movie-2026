/* Production Desk — offline cache.
   Everything here is local already, so the only job this does is let the
   installed app keep working after the launcher terminal is closed.

   Bump CACHE when any document changes, otherwise the installed app will
   keep serving the copy it cached on first run. */

const CACHE = "desk-v3";

/* crosswalk.local.js is deliberately absent from this list: it is gitignored,
   may not exist, and a single 404 fails the whole addAll(). */
const ASSETS = [
  "./",
  "./index.html",
  "./director-bible.html",
  "./production-sheet.html",
  "./lookbook-audit.html",
  "./app.webmanifest",
  "./icon.svg"
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
  if (new URL(req.url).origin !== self.location.origin) return;

  /* Cache first: these documents change only when you edit them, and being
     able to open the desk with no server running is the entire point. */
  e.respondWith(
    caches.match(req).then((hit) => {
      if (hit) {
        /* refresh in the background so an edit is picked up on the next open */
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
