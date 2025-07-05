// registerServiceWorker.js
// Registers a service worker for PWA/offline support

export function register() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js').then(
        registration => {
          // Registration successful
        },
        error => {
          // Registration failed
        }
      );
    });
  }
}
