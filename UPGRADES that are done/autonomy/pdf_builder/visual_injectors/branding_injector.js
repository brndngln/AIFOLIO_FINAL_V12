export const injectBranding = (visuals, brandLogoPath) => {
  return visuals.map(v => ({
    image: v,
    overlay: brandLogoPath
  }));
};