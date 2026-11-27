// V1.8: remove all legacy IsmaelLive caches and never serve stale assets.
self.addEventListener('install', e=>e.waitUntil(self.skipWaiting()));
self.addEventListener('activate', e=>e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith('ismael-live-'))await caches.delete(k);await self.clients.claim();})()));
// No fetch handler: all requests go directly through the browser to the server.
