const calculateLuminance = (hex) => {
  const rgb = hex
    .slice(1)
    .match(/.{2}/g)
    .map((c) => parseInt(c, 16));
  return rgb
    .map((c) => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    })
    .reduce((sum, c, i) => sum + [0.2126, 0.7152, 0.0722][i] * c, 0);
};
