import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 正式網址：Cloudflare Pages 專案名稱請取 taikeqiu，
// 之後若綁自訂網域，把下面改掉重推即可。
export default defineConfig({
  site: 'https://taikeqiu.pages.dev',
  integrations: [sitemap()],
});
