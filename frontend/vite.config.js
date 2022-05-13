import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import glob from 'glob';
import path from 'path';

const pages = glob.sync('src/**.js').reduce(function (obj, el) {
  obj[path.parse(el).name] = el;
  return obj
}, {});

// https://vitejs.dev/config/
export default defineConfig({
  mode: "development",
  plugins: [svelte()],
  build: {
    outDir: '/app/static/dist',
    emptyOutDir:true,
    sourcemap: true,
    rollupOptions: {
      input: pages,
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    }
  }
});