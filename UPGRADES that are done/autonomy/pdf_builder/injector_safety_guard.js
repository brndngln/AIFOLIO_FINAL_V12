export const enforceVisualSafety = (images = []) => {
  return images.filter((path) => {
    return path.includes("assets/visuals/") && !path.includes("external") && path.endsWith(".png");
  });
};