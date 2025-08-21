export const applyTheme = (theme, visuals) => {
  const themes = {
    dark: visuals.map((v) => v.replace(".png", "_dark.png")),
    neon: visuals.map((v) => v.replace(".png", "_neon.png")),
    luxury: visuals.map((v) => v.replace(".png", "_luxury.png")),
    zen: visuals.map((v) => v.replace(".png", "_zen.png")),
    minimalist: visuals.map((v) => v.replace(".png", "_min.png")),
  };
  return themes[theme] || visuals;
};
