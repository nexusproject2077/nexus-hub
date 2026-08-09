const CACHE = 'nexus-v7';
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
  if (e.request.method !== 'GET') return;
  // Laisser passer les requêtes externes (CDN, APIs tierces)
  if (!e.request.url.startsWith(self.location.origin)) return;

  // Les images changent rarement (et le favicon est lourd) -> CACHE-FIRST.
  const isImage =
    e.request.destination === 'image' ||
    /\.(png|jpe?g|svg|webp|ico|gif)(\?.*)?$/i.test(e.request.url);

  if (isImage) {
    e.respondWith(
      caches.match(e.request).then(cached =>
        cached ||
        fetch(e.request).then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
          return res;
        })
      )
    );
    return;
  }

  // Tout le reste (HTML, JS, CSS, JSON, /api) -> NETWORK-FIRST :
  // on affiche TOUJOURS la dernière version quand on est en ligne ;
  // le cache ne sert que de secours hors ligne. Fini le Ctrl+F5.
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
