import { defineConfig } from "vitest/config"; // [WINDSURF FIXED]

export default defineConfig({
  // [WINDSURF FIXED]
  test: {
    environment: "jsdom",
    globals: true,
  },
});
