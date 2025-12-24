import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching'
import { registerRoute } from 'workbox-routing'
import { StaleWhileRevalidate, CacheFirst, NetworkFirst } from 'workbox-strategies'
import { ExpirationPlugin } from 'workbox-expiration'

// Precache and serve static assets
precacheAndRoute(self.__WB_MANIFEST || [])

// Clean up old caches
cleanupOutdatedCaches()

// Cache strategy for different resource types

// 1. Cache static resources (CSS, JS, images) with cache-first strategy
registerRoute(
  ({ request }) => 
    request.destination === 'style' ||
    request.destination === 'script' ||
    request.destination === 'worker' ||
    request.destination === 'image',
  new CacheFirst({
    cacheName: 'static-resources',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
    ],
  })
)

// 2. Cache JSON data files with network-first strategy
registerRoute(
  ({ url }) => url.pathname.includes('/data/') || url.pathname.includes('/index.json'),
  new NetworkFirst({
    cacheName: 'data-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
      }),
    ],
  })
)

// 3. Cache PDF files with cache-first strategy (large files)
registerRoute(
  ({ request }) => request.destination === 'document' || 
    request.url.endsWith('.pdf'),
  new CacheFirst({
    cacheName: 'pdf-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 200,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
    ],
  })
)

// 4. Cache fonts and icons
registerRoute(
  ({ url }) => 
    url.pathname.includes('/fonts/') ||
    url.pathname.includes('/icons/') ||
    url.pathname.includes('.woff') ||
    url.pathname.includes('.woff2') ||
    url.pathname.includes('.ttf'),
  new CacheFirst({
    cacheName: 'font-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 30,
        maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
      }),
    ],
  })
)

// 5. Default strategy for other requests
registerRoute(
  ({ request }) => request.destination === 'document',
  new NetworkFirst({
    cacheName: 'pages-cache',
  })
)

// Handle background sync for downloads
self.addEventListener('sync', event => {
  if (event.tag === 'background-download') {
    event.waitUntil(performBackgroundDownload())
  }
})

async function performBackgroundDownload() {
  // Implement background download logic if needed
  console.log('Background download triggered')
}

// Handle push notifications (if needed in future)
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New content available',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
  }

  event.waitUntil(
    self.registration.showNotification('DSE Lib', options)
  )
})

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close()

  event.waitUntil(
    clients.openWindow('/')
  )
})

// Update strategy - notify user when new version is available
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
})

// Custom cache management
const CACHE_NAMES = {
  STATIC: 'static-resources',
  DATA: 'data-cache',
  PDF: 'pdf-cache',
  FONTS: 'font-cache',
  PAGES: 'pages-cache'
}

// Clear specific cache
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      Promise.all([
        caches.delete(CACHE_NAMES.STATIC),
        caches.delete(CACHE_NAMES.DATA),
        caches.delete(CACHE_NAMES.PDF),
        caches.delete(CACHE_NAMES.FONTS),
        caches.delete(CACHE_NAMES.PAGES),
      ])
    )
  }
})

// Log service worker events
self.addEventListener('install', event => {
  console.log('Service Worker installing')
})

self.addEventListener('activate', event => {
  console.log('Service Worker activated')
})

self.addEventListener('fetch', event => {
  // Log fetch events for debugging (remove in production)
  if (event.request.url.includes('/data/')) {
    console.log('Fetching data:', event.request.url)
  }
})