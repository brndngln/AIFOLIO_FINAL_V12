<<<<<<< HEAD
// OMNIELITE Elite License Key Manager — SAFE AI, HMAC, Audit, Revocation
import crypto from 'crypto';

const LICENSE_SECRET = process.env.AIFOLIO_LICENSE_SECRET || 'AIFOLIO_SUPER_SECRET';
const AUDIT_LOG = [];
const REVOKED_KEYS = new Set();

export function generateLicenseKey(userId, bundleId) {
  const timestamp = Date.now();
  const payload = `${userId}:${bundleId}:${timestamp}`;
  const hmac = crypto.createHmac('sha256', LICENSE_SECRET).update(payload).digest('hex');
  const key = Buffer.from(`${payload}:${hmac}`).toString('base64');
  AUDIT_LOG.push({ action: 'generate', userId, bundleId, timestamp, key });
  return key;
}

export function validateLicenseKey(key, userId, bundleId) {
  if (REVOKED_KEYS.has(key)) return false;
  try {
    const decoded = Buffer.from(key, 'base64').toString('utf8');
    const [uid, bid, timestamp, hmac] = decoded.split(':');
    if (uid !== userId || bid !== bundleId) return false;
    const payload = `${uid}:${bid}:${timestamp}`;
    const expectedHmac = crypto.createHmac('sha256', LICENSE_SECRET).update(payload).digest('hex');
    const valid = hmac === expectedHmac;
    AUDIT_LOG.push({ action: 'validate', userId, bundleId, timestamp: Date.now(), key, valid });
    return valid;
  } catch (e) {
    AUDIT_LOG.push({ action: 'validate-fail', userId, bundleId, timestamp: Date.now(), key, error: e.message });
    return false;
  }
}

export function revokeLicenseKey(key, adminId) {
  REVOKED_KEYS.add(key);
  AUDIT_LOG.push({ action: 'revoke', adminId, key, timestamp: Date.now() });
}

export function getAuditLog() {
  return [...AUDIT_LOG];
}

export function exportAuditLog(format = 'json') {
  if (format === 'csv') {
    const rows = AUDIT_LOG.map(e => Object.values(e).map(v => JSON.stringify(v)).join(','));
    return ['action,userId,bundleId,timestamp,key,valid,adminId,error', ...rows].join('\n');
  }
  return JSON.stringify(AUDIT_LOG, null, 2);
}

=======
// OMNIELITE License Key Manager for Template Resale Bundles — Elite, SAFE AI, Owner-Controlled, Auditable
const crypto = require('crypto');
const AUDIT_LOG = [];

/**
 * Deterministically generate a license key for a vault bundle.
 * Uses HMAC with SHA256 for static, owner-controlled, SAFE AI-compliant licensing.
 * All logic is static, non-adaptive, and fully auditable.
 */
function generateLicenseKey(userId, bundleId) {
  const secret = process.env.AIFOLIO_LICENSE_SECRET || 'AIFOLIO_OWNER_SECRET';
  const data = `${userId}:${bundleId}`;
  const hmac = crypto.createHmac('sha256', secret).update(data).digest('hex');
  const key = `${bundleId.toUpperCase().slice(0,4)}-${hmac.slice(0,8)}-${userId.slice(0,4).toUpperCase()}`;
  AUDIT_LOG.push({ action: 'generate', userId, bundleId, key, timestamp: Date.now() });
  return key;
}

/**
 * Validate a deterministic license key for a vault bundle.
 * All validation is static, SAFE AI-compliant, and owner-controlled.
 * Returns true if valid, false otherwise. Logs all attempts for audit.
 */
function validateLicenseKey(key, userId, bundleId) {
  const expected = generateLicenseKey(userId, bundleId);
  const valid = (key === expected);
  AUDIT_LOG.push({ action: 'validate', userId, bundleId, key, valid, timestamp: Date.now() });
  return valid;
}

/**
 * Export audit log for compliance review.
 */
function exportAuditLog() {
  return [...AUDIT_LOG];
}

module.exports = {
  generateLicenseKey,
  validateLicenseKey,
  exportAuditLog
};
>>>>>>> 151a0d1 (🧼 Cleaned repo: removed nested Git repos from backups, staged all elite changes)
