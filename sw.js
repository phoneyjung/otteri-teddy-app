// Service Worker - ทำให้ทำงานออฟไลน์ได้ + cache assets
// v4: เปลี่ยนเป็น network-first สำหรับ HTML (ให้ได้โค้ดใหม่เสมอ)
//     และ cache-first สำหรับ assets อื่น (icon, manifest)
const CACHE_NAME = 'plp-laundry-v4';
const urlsToCache = [
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-180.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = event.request.url;

  // อย่า cache Firebase/Firestore requests (ต้อง live)
  if (url.includes('firestore.googleapis.com') ||
      url.includes('firebase') ||
      url.includes('googleapis.com')) {
    return; // ปล่อยให้ browser handle เอง
  }

  // HTML / root: network-first (ได้โค้ดใหม่ทุกครั้งถ้ามีเน็ต)
  // ถ้าไม่มีเน็ต ค่อย fallback ไป cache
  const isHTML = event.request.mode === 'navigate' ||
                 url.endsWith('/') ||
                 url.endsWith('.html');

  if (isHTML) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Save fresh copy to cache
          const cloned = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, cloned));
          return response;
        })
        .catch(() => caches.match(event.request).then(r => r || caches.match('./index.html')))
    );
    return;
  }

  // อื่นๆ (รูปภาพ, manifest, fonts): cache-first
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response) return response;
      return fetch(event.request).then((networkResponse) => {
        // Cache successful responses
        if (networkResponse.ok) {
          const cloned = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, cloned));
        }
        return networkResponse;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
