import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 5173,  // Chỉnh sửa cổng ở đây
  },
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
