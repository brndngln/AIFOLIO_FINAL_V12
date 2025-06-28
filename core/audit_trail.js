// OMNIELITE AIFOLIO - Static Audit Trail Logger
// SAFE AI-compliant, deterministic, owner-controlled, and fully auditable
const fs = require('fs');
const path = require('path');

const AUDIT_DIR = path.resolve(__dirname, '../audit/exports');
if (!fs.existsSync(AUDIT_DIR)) fs.mkdirSync(AUDIT_DIR, { recursive: true });

function logAudit(module, action, details) {
  const entry = {
    timestamp: new Date().toISOString(),
    module,
    action,
    details,
    static: true
  };
  const file = path.join(AUDIT_DIR, `${module}_audit.json`);
  let arr = [];
  if (fs.existsSync(file)) {
    try { arr = JSON.parse(fs.readFileSync(file, 'utf-8')); } catch (e) { arr = []; }
  }
  arr.push(entry);
  fs.writeFileSync(file, JSON.stringify(arr, null, 2));
}

function exportAudit(module, format = 'json') {
  const file = path.join(AUDIT_DIR, `${module}_audit.json`);
  if (!fs.existsSync(file)) return null;
  const arr = JSON.parse(fs.readFileSync(file, 'utf-8'));
  if (format === 'csv') {
    const keys = Object.keys(arr[0] || {});
    const csv = [keys.join(',')].concat(arr.map(e => keys.map(k => JSON.stringify(e[k]||'')).join(','))).join('\n');
    return csv;
  }
  return JSON.stringify(arr, null, 2);
}

module.exports = { logAudit, exportAudit };
