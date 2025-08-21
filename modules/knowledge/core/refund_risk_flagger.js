// Static Refund-Risk Flagger - SAFE AI, deterministic, owner-controlled
// Flags high-risk phrases or patterns in a static, auditable way
function flagRefundRisk(text) {
  const risks = [];
  if (/money back guarantee/i.test(text))
    risks.push("Mentions money-back guarantee");
  if (/no questions asked/i.test(text))
    risks.push("Mentions no-questions-asked refund");
  // ...add more static rules as needed
  return {
    risks,
    audit: { checkedAt: new Date().toISOString(), static: true },
  };
}
module.exports = { flagRefundRisk };
