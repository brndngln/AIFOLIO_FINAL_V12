// OMNIELITE Elite License Key Manager — SAFE AI, HMAC, Audit, Revocation
import crypto from "crypto";

const LICENSE_SECRET =
  process.env.AIFOLIO_LICENSE_SECRET || "AIFOLIO_SUPER_SECRET";
const AUDIT_LOG = [];
const REVOKED_KEYS = new Set();

export function generateLicenseKey(userId, bundleId) {
  const timestamp = Date.now();
  const payload = `${userId}:${bundleId}:${timestamp}`;
  const hmac = crypto
    .createHmac("sha256", LICENSE_SECRET)
    .update(payload)
    .digest("hex");
  const key = Buffer.from(`${payload}:${hmac}`).toString("base64");
  AUDIT_LOG.push({ action: "generate", userId, bundleId, timestamp, key });
  return key;
}

export function validateLicenseKey(key, userId, bundleId) {
  if (REVOKED_KEYS.has(key)) return false;
  try {
    const decoded = Buffer.from(key, "base64").toString("utf8");
    const [uid, bid, timestamp, hmac] = decoded.split(":");
    if (uid !== userId || bid !== bundleId) return false;
    const payload = `${uid}:${bid}:${timestamp}`;
    const expectedHmac = crypto
      .createHmac("sha256", LICENSE_SECRET)
      .update(payload)
      .digest("hex");
    const valid = hmac === expectedHmac;
    AUDIT_LOG.push({
      action: "validate",
      userId,
      bundleId,
      timestamp: Date.now(),
      key,
      valid,
    });
    return valid;
  } catch (e) {
    AUDIT_LOG.push({
      action: "validate-fail",
      userId,
      bundleId,
      timestamp: Date.now(),
      key,
      error: e.message,
    });
    return false;
  }
}

export function revokeLicenseKey(key, adminId) {
  REVOKED_KEYS.add(key);
  AUDIT_LOG.push({ action: "revoke", adminId, key, timestamp: Date.now() });
}

export function getAuditLog() {
  return [...AUDIT_LOG];
}

export function exportAuditLog(format = "json") {
  if (format === "csv") {
    const rows = AUDIT_LOG.map((e) =>
      Object.values(e)
        .map((v) => JSON.stringify(v))
        .join(","),
    );
    return [
      "action,userId,bundleId,timestamp,key,valid,adminId,error",
      ...rows,
    ].join("\n");
  }
  return JSON.stringify(AUDIT_LOG, null, 2);
}
