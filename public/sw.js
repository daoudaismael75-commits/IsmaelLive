// V1.9: no offline caching of authenticated content.
self.addEventListener('install',e=>e.waitUntil(self.skipWaiting()));
self.addEventListener('activate',e=>e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith('ismael-live-'))await caches.delete(k);await self.clients.claim()})()));
