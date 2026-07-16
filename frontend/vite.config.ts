import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    hmr: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    // Enable CSS code splitting
    cssCodeSplit: true,
    // Source maps for production debugging (but not for users)
    sourcemap: false,
    // Minify with esbuild for speed
    minify: 'esbuild',
    // Rollup options for manual chunk splitting
    rollupOptions: {
      output: {
        manualChunks(id: string) {
          if (id.includes('node_modules/react-dom') || id.includes('node_modules/react-router')) {
            return 'react-vendor';
          }
          if (id.includes('node_modules/framer-motion')) {
            return 'animation-vendor';
          }
          if (id.includes('node_modules/recharts')) {
            return 'chart-vendor';
          }
          if (id.includes('node_modules/lucide-react')) {
            return 'icons-vendor';
          }
        },
      },
    },
    // Target modern browsers for smaller bundles
    target: 'es2021',
    // Increase chunk size warning limit (we know what we're doing)
    chunkSizeWarningLimit: 1000,
  },
})
