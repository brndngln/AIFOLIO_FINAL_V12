<<<<<<< HEAD
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/setupTests.js']
=======
import { defineConfig } from "vitest/config"; // [WINDSURF FIXED]

export default defineConfig({ // [WINDSURF FIXED]
  test: {
    environment: 'jsdom',
    globals: true,
>>>>>>> omni_repair_backup_20250704_1335
  },
});
