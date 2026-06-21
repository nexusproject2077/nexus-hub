const CACHE = 'nexus-v6';
const ASSETS = [
  './',
  './index.html',
  './archive.html',
  './blog.html',
  './projets.html',
  './competences.html',
  './cv.html',
  './nexus-base.css',
  './nexus-shared.js',
  './manifest.json',
  './favicon.png',
  './followers_data.json',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Laisser passer les requêtes externes (CDN, APIs)
  if (!e.request.url.startsWith(self.location.origin)) return;

  const isHTML =
    e.request.mode === 'navigate' ||
    e.request.destination === 'document' ||
    e.request.url.endsWith('.html') ||
    e.request.url.endsWith('/');

  if (isHTML) {
    // NETWORK-FIRST : toujours la dernière version, cache en secours (hors ligne)
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
  } else {
    // CACHE-FIRST : pour CSS, JS, images (rapide)
    e.respondWith(
      caches.match(e.request).then(cached => cached || fetch(e.request))
    );
  }
});
