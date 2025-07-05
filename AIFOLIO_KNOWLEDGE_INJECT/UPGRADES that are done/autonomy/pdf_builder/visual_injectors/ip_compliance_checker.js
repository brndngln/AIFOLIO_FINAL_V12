export const checkImageRights = (visuals) => {
  return visuals.map(v => ({
    image: v,
    approved: !v.includes('unlicensed')
  }));
};
