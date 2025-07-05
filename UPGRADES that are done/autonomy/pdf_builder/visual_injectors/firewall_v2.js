export const scanVisualsForLeaks = (visuals) => {
  return visuals.filter(v => !(v.includes('external') || v.includes('unverified')));
};
