const CACHE = 'nexus-v3';

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
  // Pass through external requests (CDN, APIs)
  if (!e.request.url.startsWith(self.location.origin)) return;

  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
