// AIFOLIO Elite System - Service Worker
// Version: 1.0.0
// Cache Strategy: Network First with Fallback

const CACHE_NAME = 'aifolio-elite-v1.0.0';
const OFFLINE_URL = '/offline.html';

// Assets to cache on install
const STATIC_CACHE_URLS = [
  '/',
  '/offline.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// Dynamic cache patterns
const CACHE_PATTERNS = {
  api: /^https:\/\/api\./,
  assets: /\.(js|css|png|jpg|jpeg|gif|svg|woff|woff2)$/,
  pages: /^https?:\/\/[^\/]+\/(?!api)/
};

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('🔋 AIFOLIO SW: Installing...');

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('🔋 AIFOLIO SW: Caching static assets');
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        console.log('🔋 AIFOLIO SW: Installation complete');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('🔋 AIFOLIO SW: Installation failed:', error);
      })
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  console.log('🔋 AIFOLIO SW: Activating...');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              console.log('🔋 AIFOLIO SW: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('🔋 AIFOLIO SW: Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - network first with cache fallback
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension and other protocols
  if (!url.protocol.startsWith('http')) {
    return;
  }

  event.respondWith(
    handleFetchRequest(request)
  );
});

async function handleFetchRequest(request) {
  const url = new URL(request.url);

  try {
    // Network first strategy
    const networkResponse = await fetch(request);

    // Cache successful responses
    if (networkResponse.status === 200) {
      const cache = await caches.open(CACHE_NAME);

      // Cache based on content type
      if (shouldCache(request)) {
        cache.put(request, networkResponse.clone());
      }
    }

    return networkResponse;

  } catch (error) {
    console.log('🔋 AIFOLIO SW: Network failed, trying cache:', url.pathname);

    // Try cache fallback
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      const offlineResponse = await caches.match(OFFLINE_URL);
      if (offlineResponse) {
        return offlineResponse;
      }
    }

    // Return generic offline response
    return new Response(
      JSON.stringify({
        error: 'Offline',
        message: 'Network unavailable and no cached version found',
        timestamp: new Date().toISOString()
      }),
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache'
        }
      }
    );
  }
}

function shouldCache(request) {
  const url = new URL(request.url);

  // Cache static assets
  if (CACHE_PATTERNS.assets.test(url.pathname)) {
    return true;
  }

  // Cache API responses (with TTL)
  if (CACHE_PATTERNS.api.test(url.hostname)) {
    return true;
  }

  // Cache page navigation
  if (request.mode === 'navigate') {
    return true;
  }

  return false;
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('🔋 AIFOLIO SW: Background sync triggered:', event.tag);

  if (event.tag === 'vault-sync') {
    event.waitUntil(syncVaultData());
  }
});

async function syncVaultData() {
  try {
    // Placeholder for future vault synchronization
    console.log('🔋 AIFOLIO SW: Vault sync placeholder - ready for implementation');

    // This will be expanded when vault backend is integrated
    const syncData = await getStoredSyncData();
    if (syncData && syncData.length > 0) {
      // Process sync queue
      console.log('🔋 AIFOLIO SW: Processing sync queue:', syncData.length, 'items');
    }
  } catch (error) {
    console.error('🔋 AIFOLIO SW: Vault sync failed:', error);
  }
}

async function getStoredSyncData() {
  // Placeholder for IndexedDB or localStorage sync queue
  return [];
}

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('🔋 AIFOLIO SW: Push notification received');

  const options = {
    body: event.data ? event.data.text() : 'AIFOLIO notification',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Open AIFOLIO',
        icon: '/icons/icon-192x192.png'
      },
      {
        action: 'close',
        title: 'Dismiss',
        icon: '/icons/close.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('AIFOLIO Elite System', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('🔋 AIFOLIO SW: Notification clicked:', event.action);

  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

console.log('🔋 AIFOLIO SW: Service Worker loaded and ready');
