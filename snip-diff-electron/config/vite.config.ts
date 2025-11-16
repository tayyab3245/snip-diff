import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  base: './',
  root: resolve(__dirname, '../src/ui'),
  publicDir: resolve(__dirname, '../public'),
  build: {
    outDir: resolve(__dirname, '../dist/ui'),
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    strictPort: true,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, '../src/ui'),
      '@shared': resolve(__dirname, '../src/shared'),
    },
  },
});
