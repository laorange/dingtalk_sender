import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver, NaiveUiResolver, VantResolver} from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    Components({
      resolvers: [ElementPlusResolver(), NaiveUiResolver(), VantResolver()],
    }),
    vue(),
  ]
})
