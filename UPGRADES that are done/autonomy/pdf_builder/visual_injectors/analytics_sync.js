export const syncVisualWithAnalytics = (visualPath, stats) => {
  return {
    path: visualPath,
    views: stats.views[visualPath] || 0,
    clicks: stats.clicks[visualPath] || 0,
    conversions: stats.conversions[visualPath] || 0
  };
};