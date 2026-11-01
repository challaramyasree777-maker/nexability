import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "https://blaspheme-vending-wilt.ngrok-free.dev",
        changeOrigin: true,
        headers: {
          "ngrok-skip-browser-warning": "1",
        },
      },
    },
  },
});
