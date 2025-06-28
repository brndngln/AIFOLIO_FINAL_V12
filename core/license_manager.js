// OMNIELITE License Key Manager for Template Resale Bundles
export function generateLicenseKey(userId, bundleId) {
  // Simple deterministic license key (expand for production)
  return btoa(`${userId}:${bundleId}:${Date.now()}`).slice(0, 24);
}

export function validateLicenseKey(key, userId, bundleId) {
  // Placeholder: In production, add cryptographic validation
  return key.startsWith(btoa(`${userId}:${bundleId}`).slice(0, 8));
}
