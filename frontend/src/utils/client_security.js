// Client-side CSRF/XSS/validation utilities
export function sanitizeInput(input) {
  // Basic escaping for XSS
  return String(input)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export function validateForm(fields) {
  // Example: require all fields non-empty and max 256 chars
  for (const key in fields) {
    if (!fields[key] || fields[key].length > 256) return false;
  }
  return true;
}

export function getCSRFToken() {
  // Example: fetch from meta tag or cookie
  const el = document.querySelector('meta[name="csrf-token"]');
  return el ? el.content : '';
}
