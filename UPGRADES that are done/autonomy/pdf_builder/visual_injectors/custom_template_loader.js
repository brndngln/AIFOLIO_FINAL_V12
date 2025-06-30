export const loadCustomVisuals = (nicheName, basePath = "assets/custom_visuals/") => {
  return [
    basePath + nicheName + "/template1.png",
    basePath + nicheName + "/template2.png",
    basePath + nicheName + "/template3.png"
  ];
};