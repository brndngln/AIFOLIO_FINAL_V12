export const triggerVisualAlert = (condition, message) => {
  if (condition) {
    console.warn('[VISUAL ALERT]', message);
  }
};