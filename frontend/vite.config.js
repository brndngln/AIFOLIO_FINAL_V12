import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  root: ".", // Vite project root
  publicDir: "public", // Static assets directory
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"), // Allows imports like: import Button from '@/components/Button'
    },
  },
  server: {
    port: 5173, // Dev server port
    open: true, // Auto open browser on dev
  },
  build: {
    outDir: "dist", // Default output folder
    emptyOutDir: true, // Clears old build
  },
});
