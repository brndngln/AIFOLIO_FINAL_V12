// Static Visual Balance Checker - SAFE AI, deterministic, owner-controlled
// Checks for static layout issues in a JSON-based design spec
function checkVisualBalance(designSpec) {
  // Example: Flag if any section width is > 70% or < 20%
  const issues = [];
  (designSpec.sections || []).forEach((section, i) => {
    if (section.width > 0.7) issues.push({ section: i, issue: 'Too wide' });
    if (section.width < 0.2) issues.push({ section: i, issue: 'Too narrow' });
  });
  return { issues, audit: { checkedAt: new Date().toISOString(), static: true } };
}
module.exports = { checkVisualBalance };
