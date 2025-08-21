// Static Marketplace Trend Analyzer - SAFE AI, deterministic, owner-controlled
// Flags static keywords for trending topics
function analyzeTrends(text) {
  const trends = [];
  if (/ai/i.test(text)) trends.push("AI");
  if (/automation/i.test(text)) trends.push("Automation");
  if (/side hustle/i.test(text)) trends.push("Side Hustle");
  // ...add more static rules as needed
  return {
    trends,
    audit: { checkedAt: new Date().toISOString(), static: true },
  };
}
module.exports = { analyzeTrends };
