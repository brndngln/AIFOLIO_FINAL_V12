// Static Typo/Grammar Checker - SAFE AI, deterministic, owner-controlled
// Returns flagged issues in a static, auditable format
function checkText(text) {
  // Example: Only flag common mistakes, no adaptive logic
  const issues = [];
  if (/\bteh\b/i.test(text)) issues.push({ type: 'typo', word: 'teh', suggestion: 'the' });
  if (/\brecieve\b/i.test(text)) issues.push({ type: 'typo', word: 'recieve', suggestion: 'receive' });
  if (/\bdefinately\b/i.test(text)) issues.push({ type: 'typo', word: 'definately', suggestion: 'definitely' });
  // ...add more static rules as needed
  return { issues, audit: { checkedAt: new Date().toISOString(), static: true } };
}
module.exports = { checkText };
