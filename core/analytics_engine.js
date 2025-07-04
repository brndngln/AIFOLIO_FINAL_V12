// OMNIELITE Analytics Engine: Tracks drops, usage, downloads, ROI, leaderboard
const analyticsStore = {};

export function logEvent(vaultId, eventType, data) {
  if (!analyticsStore[vaultId]) analyticsStore[vaultId] = [];
  analyticsStore[vaultId].push({ eventType, data, timestamp: Date.now() });
}

export function getVaultStats(vaultId) {
  const events = analyticsStore[vaultId] || [];
  return {
    dropsCreated: events.filter(e => e.eventType === 'drop').length,
    promptUsage: events.filter(e => e.eventType === 'prompt').length,
    pdfDownloads: events.filter(e => e.eventType === 'pdf_download').length,
    exportTypes: [...new Set(events.filter(e => e.eventType === 'export').map(e => e.data.type))],
    leaderboard: Object.entries(analyticsStore)
      .map(([id, evs]) => ({ id, drops: evs.filter(e => e.eventType === 'drop').length }))
      .sort((a, b) => b.drops - a.drops)
  };
}

export function getLeaderboard() {
  return Object.entries(analyticsStore)
    .map(([id, evs]) => ({ id, drops: evs.filter(e => e.eventType === 'drop').length }))
    .sort((a, b) => b.drops - a.drops);
}
