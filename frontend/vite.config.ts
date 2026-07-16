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
        manualChunks: {
          // React core
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          // Animation
          'animation-vendor': ['framer-motion'],
          // Charts
          'chart-vendor': ['recharts'],
          // Icons
          'icons-vendor': ['lucide-react'],
        },
      },
    },
    // Target modern browsers for smaller bundles
    target: 'es2021',
    // Increase chunk size warning limit (we know what we're doing)
    chunkSizeWarningLimit: 1000,
  },
})
