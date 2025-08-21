// Static Asset Health Checker - SAFE AI, deterministic, owner-controlled
// Checks for static asset file presence and basic metadata
const fs = require("fs");
function checkAssetHealth(assetPath) {
  let exists = false;
  let size = 0;
  try {
    const stats = fs.statSync(assetPath);
    exists = stats.isFile();
    size = stats.size;
  } catch (e) {}
  return {
    exists,
    size,
    audit: { checkedAt: new Date().toISOString(), static: true },
  };
}
module.exports = { checkAssetHealth };
