// vite.config.js
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      '/genpwd':   'http://localhost:8000',
      '/gen2fa':   'http://localhost:8000',
      '/authuser': 'http://localhost:8000',
      '/request-reset':  'http://localhost:8000',
      '/reset-password':'http://localhost:8000',
    }
  }
})
