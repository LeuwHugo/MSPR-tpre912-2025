import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      // sans slash
      '/function': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false
      },
      // avec slash (au cas où)
      '/function/': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
