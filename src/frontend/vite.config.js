import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path';
import dotenv from 'dotenv';

// https://vitejs.dev/config/
const envPath = path.resolve(__dirname, '../../.env');
dotenv.config({ path: envPath });

export default defineConfig({
  plugins: [react()],
  define: {
    'process.env': process.env,
  },
  resolve: {
    alias: {
      '@public': path.resolve(__dirname, 'public'),
      '@utils': path.resolve(__dirname, 'src/utils'),
      '@context': path.resolve(__dirname, 'src/context'),
      '@assets': path.resolve(__dirname, 'src/assets'),
      '@constants': path.resolve(__dirname, 'src/constants'),
      //client
      '@client': path.resolve(__dirname, 'src/client'),
      '@client/styles': path.resolve(__dirname, 'src/client/styles'),
      '@client/routers': path.resolve(__dirname, 'src/client/routers'),
      '@client/pages': path.resolve(__dirname, 'src/client/pages'),
      // '@client/context': path.resolve(__dirname, 'src/client/context'),
      '@client/components': path.resolve(__dirname, 'src/client/components'),
      //admin
      '@admin': path.resolve(__dirname, 'src/admin'),
      '@admin/styles': path.resolve(__dirname, 'src/admin/styles'),
      '@admin/routers': path.resolve(__dirname, 'src/admin/routers'),
      '@admin/pages': path.resolve(__dirname, 'src/admin/pages'),
      // '@admin/context': path.resolve(__dirname, 'src/admin/context'),
      '@admin/components': path.resolve(__dirname, 'src/admin/components'),
      // '@admin/assets': path.resolve(__dirname, 'src/admin/assets'),

      '@theme': path.resolve(__dirname, 'theme.js'),

    },
  },
 
})
