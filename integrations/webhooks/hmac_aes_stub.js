// OMNIELITE AIFOLIO - Webhook HMAC/AES Stub
// SAFE AI-compliant, deterministic, owner-controlled, and fully auditable
const crypto = require('crypto');
function signPayload(payload, secret) {
  // Static HMAC-SHA256 signature
  return crypto.createHmac('sha256', secret).update(JSON.stringify(payload)).digest('hex');
}
function aesEncrypt(payload, secret) {
  // Static AES-256-CBC encryption stub (for demo/testing)
  const iv = Buffer.alloc(16, 0); // static IV for deterministic output
  const key = crypto.createHash('sha256').update(secret).digest();
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  let encrypted = cipher.update(JSON.stringify(payload), 'utf8', 'base64');
  encrypted += cipher.final('base64');
  return encrypted;
}
module.exports = { signPayload, aesEncrypt };
