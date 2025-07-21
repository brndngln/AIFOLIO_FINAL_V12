// AIFOLIO Elite System - Service Worker Registration
// Advanced PWA integration with install prompt handling

const isLocalhost = Boolean(
  window.location.hostname === 'localhost' ||
  window.location.hostname === '[::1]' ||
  window.location.hostname.match(
    /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/
  )
);

// Store install prompt for later use
let deferredPrompt;

export function register(config) {
  if ('serviceWorker' in navigator) {
    // Register service worker
    window.addEventListener('load', () => {
      const swUrl = '/sw.js';

      if (isLocalhost) {
        // Development environment
        checkValidServiceWorker(swUrl, config);

        navigator.serviceWorker.ready.then(() => {
          console.log('🔋 AIFOLIO SW: Development mode - service worker ready');
        });
      } else {
        // Production environment
        registerValidSW(swUrl, config);
      }
    });

    // Handle install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      console.log('🔋 AIFOLIO PWA: Install prompt available');

      // Prevent Chrome 67 and earlier from automatically showing the prompt
      e.preventDefault();

      // Stash the event so it can be triggered later
      deferredPrompt = e;

      // Update UI to notify the user they can add to home screen
      showInstallPromotion();
    });

    // Handle successful installation
    window.addEventListener('appinstalled', (evt) => {
      console.log('🔋 AIFOLIO PWA: App successfully installed');

      // Hide install promotion
      hideInstallPromotion();

      // Track installation event
      if (typeof gtag !== 'undefined') {
        gtag('event', 'pwa_install', {
          event_category: 'PWA',
          event_label: 'App Installed'
        });
      }

      // Notify user
      showInstallSuccess();
    });
  } else {
    console.warn('🔋 AIFOLIO PWA: Service workers not supported');
  }
}

function registerValidSW(swUrl, config) {
  navigator.serviceWorker
    .register(swUrl)
    .then((registration) => {
      console.log('🔋 AIFOLIO SW: Registered successfully:', registration.scope);

      registration.onupdatefound = () => {
        const installingWorker = registration.installing;
        if (installingWorker == null) {
          return;
        }

        installingWorker.onstatechange = () => {
          if (installingWorker.state === 'installed') {
            if (navigator.serviceWorker.controller) {
              // New content is available
              console.log('🔋 AIFOLIO SW: New content available, please refresh');

              if (config && config.onUpdate) {
                config.onUpdate(registration);
              }

              showUpdateAvailable();
            } else {
              // Content is cached for offline use
              console.log('🔋 AIFOLIO SW: Content cached for offline use');

              if (config && config.onSuccess) {
                config.onSuccess(registration);
              }
            }
          }
        };
      };
    })
    .catch((error) => {
      console.error('🔋 AIFOLIO SW: Registration failed:', error);
    });
}

function checkValidServiceWorker(swUrl, config) {
  // Check if the service worker can be found
  fetch(swUrl, {
    headers: { 'Service-Worker': 'script' },
  })
    .then((response) => {
      const contentType = response.headers.get('content-type');
      if (
        response.status === 404 ||
        (contentType != null && contentType.indexOf('javascript') === -1)
      ) {
        // Service worker not found, reload the page
        navigator.serviceWorker.ready.then((registration) => {
          registration.unregister().then(() => {
            window.location.reload();
          });
        });
      } else {
        // Service worker found, proceed normally
        registerValidSW(swUrl, config);
      }
    })
    .catch(() => {
      console.log('🔋 AIFOLIO SW: No internet connection, running in offline mode');
    });
}

export function unregister() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then((registration) => {
        registration.unregister();
        console.log('🔋 AIFOLIO SW: Unregistered successfully');
      })
      .catch((error) => {
        console.error('🔋 AIFOLIO SW: Unregistration failed:', error);
      });
  }
}

// PWA Install Promotion Functions
function showInstallPromotion() {
  // Create install button if it doesn't exist
  let installButton = document.getElementById('pwa-install-button');

  if (!installButton) {
    installButton = document.createElement('button');
    installButton.id = 'pwa-install-button';
    installButton.innerHTML = '📱 Install App';
    installButton.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 25px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(0,0,0,0.2);
      z-index: 1000;
      transition: all 0.3s ease;
      backdrop-filter: blur(10px);
    `;

    installButton.addEventListener('mouseenter', () => {
      installButton.style.transform = 'translateY(-2px)';
      installButton.style.boxShadow = '0 6px 20px rgba(0,0,0,0.3)';
    });

    installButton.addEventListener('mouseleave', () => {
      installButton.style.transform = 'translateY(0)';
      installButton.style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)';
    });

    installButton.addEventListener('click', promptInstall);
    document.body.appendChild(installButton);
  }

  // Animate in
  installButton.style.opacity = '0';
  installButton.style.transform = 'translateY(100px)';

  setTimeout(() => {
    installButton.style.transition = 'all 0.5s ease';
    installButton.style.opacity = '1';
    installButton.style.transform = 'translateY(0)';
  }, 100);
}

function hideInstallPromotion() {
  const installButton = document.getElementById('pwa-install-button');
  if (installButton) {
    installButton.style.opacity = '0';
    installButton.style.transform = 'translateY(100px)';

    setTimeout(() => {
      installButton.remove();
    }, 500);
  }
}

async function promptInstall() {
  if (deferredPrompt) {
    console.log('🔋 AIFOLIO PWA: Showing install prompt');

    // Show the prompt
    deferredPrompt.prompt();

    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`🔋 AIFOLIO PWA: User response: ${outcome}`);

    if (outcome === 'accepted') {
      console.log('🔋 AIFOLIO PWA: User accepted the install prompt');
    } else {
      console.log('🔋 AIFOLIO PWA: User dismissed the install prompt');
    }

    // Clear the deferredPrompt
    deferredPrompt = null;

    // Hide the install button
    hideInstallPromotion();
  }
}

function showUpdateAvailable() {
  // Create update notification
  const updateNotification = document.createElement('div');
  updateNotification.id = 'pwa-update-notification';
  updateNotification.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between;">
      <span>🔄 New version available!</span>
      <button id="pwa-update-button" style="
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        cursor: pointer;
        margin-left: 16px;
      ">Update</button>
    </div>
  `;

  updateNotification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(0,0,0,0.8);
    color: white;
    padding: 16px 20px;
    border-radius: 10px;
    font-size: 14px;
    z-index: 1001;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
  `;

  document.body.appendChild(updateNotification);

  // Handle update button click
  document.getElementById('pwa-update-button').addEventListener('click', () => {
    window.location.reload();
  });

  // Auto-hide after 10 seconds
  setTimeout(() => {
    if (updateNotification.parentNode) {
      updateNotification.remove();
    }
  }, 10000);
}

function showInstallSuccess() {
  // Create success notification
  const successNotification = document.createElement('div');
  successNotification.innerHTML = '✅ AIFOLIO installed successfully!';
  successNotification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    padding: 16px 20px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    z-index: 1001;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  `;

  document.body.appendChild(successNotification);

  // Auto-hide after 5 seconds
  setTimeout(() => {
    successNotification.style.opacity = '0';
    successNotification.style.transform = 'translateX(100%)';

    setTimeout(() => {
      if (successNotification.parentNode) {
        successNotification.remove();
      }
    }, 500);
  }, 5000);
}

// Export install prompt function for manual triggering
export { promptInstall };

console.log('🔋 AIFOLIO PWA: Registration module loaded');
