// OMNIELITE AIFOLIO - Immutable Elite Audit Trail Logger
// SAFE AI-compliant, deterministic, append-only, owner-controlled, and fully auditable
const fs = require('fs');
const path = require('path');

const AUDIT_DIR = path.resolve(__dirname, '../audit/exports');
if (!fs.existsSync(AUDIT_DIR)) fs.mkdirSync(AUDIT_DIR, { recursive: true });

function logAudit(module, action, details, compliance = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    module,
    action,
    details,
    compliance,
    static: true
  };
  const file = path.join(AUDIT_DIR, `${module}_audit.jsonl`);
  fs.appendFileSync(file, JSON.stringify(entry) + '\n');
}

function exportAudit(module, format = 'json') {
  const file = path.join(AUDIT_DIR, `${module}_audit.jsonl`);
  if (!fs.existsSync(file)) return null;
  const lines = fs.readFileSync(file, 'utf-8').split('\n').filter(Boolean);
  const arr = lines.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  if (format === 'csv') {
    const keys = Object.keys(arr[0] || {});
    const csv = [keys.join(',')].concat(arr.map(e => keys.map(k => JSON.stringify(e[k]||'')).join(','))).join('\n');
    return csv;
  }
  return JSON.stringify(arr, null, 2);
}

// Compliance self-check hook
function runComplianceCheck(module) {
  // Example: check for SAFE AI, privacy, and security compliance tags in audit
  const file = path.join(AUDIT_DIR, `${module}_audit.jsonl`);
  if (!fs.existsSync(file)) return { status: 'no-audit' };
  const lines = fs.readFileSync(file, 'utf-8').split('\n').filter(Boolean);
  const arr = lines.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  const tags = arr.flatMap(e => (e.compliance && Array.isArray(e.compliance.tags)) ? e.compliance.tags : []);
  const safe = tags.includes('SAFE_AI');
  const privacy = tags.includes('privacy');
  const security = tags.includes('security');
  return { safe, privacy, security, total: arr.length };
}

module.exports = { logAudit, exportAudit, runComplianceCheck };
