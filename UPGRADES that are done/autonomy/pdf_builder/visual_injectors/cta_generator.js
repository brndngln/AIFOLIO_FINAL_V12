export const generateCTABanners = (ctaList) => {
  return ctaList.map(text => ({
    type: 'cta-banner',
    content: text,
    style: 'highlighted'
  }));
};