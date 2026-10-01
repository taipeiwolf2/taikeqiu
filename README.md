# 台客秋 — Astro 新品牌站

獨立品牌優惠整理站（Astro 靜態產生 + Cloudflare Pages 免費託管 + GitHub 自動建置）。
2026-10-01 決策：kb56.tw 部分廠商不再提供分潤資源，台客秋重建為獨立品牌，
不再掛 kb56.tw 資料來源。

## 網址

- 正式站：https://taikeqiu.pages.dev（Cloudflare Pages 專案名稱取 `taikeqiu`）
- 之後若綁自訂網域，改 `astro.config.mjs` 的 `site` 後重推即可
- 舊站（待退役）：https://sites.google.com/view/joe-ho-deals

## 專案結構

```
src/data/promos.json      ← 優惠資料（由 tools/build_promos.py 從 deals-sync 產生）
src/layouts/Layout.astro  ← 共用版型：SEO meta、導覽、頁尾、複製碼 JS
src/components/DealCard.astro
src/pages/index.astro     ← 首頁（hero、TOP 5、三大專區卡）
src/pages/[category].astro← /delivery/ /taxi/ /travel/（由 promos.json 動態產生）
public/robots.txt、public/favicon.svg
tools/build_promos.py     ← 資料轉換：deals-sync/*.py → promos.json
tools/push_to_github.py   ← 建 repo＋推檔（需 GitHub token，見下）
```

## 指令

```bash
npm install
npm run dev      # 本地預覽
npm run build    # 產生 dist/
```

## 資料更新流程（每月／有新優惠時）

1. 更新 `~/workspace/deals-sync/` 的資料檔（deals_data.py 等）
2. `cd ~/workspace/taikeqiu && python3 tools/build_promos.py`（169 檔 → promos.json）
3. `npm run build` 本地驗證
4. `python3 tools/push_to_github.py` 推上 GitHub → Cloudflare Pages 自動重建（約 1 分鐘）

## Cloudflare Pages 接線（一次性，使用者手動）

1. 登入 https://dash.cloudflare.com → Pages → Create → Connect to Git
2. 選 GitHub repo `taikeqiu`
3. Framework preset 選 Astro；Build command `npm run build`；Output `dist`
4. Deploy → 拿到 https://taikeqiu.pages.dev

## SEO 現況

- 每頁獨立 title / meta description / canonical / OG
- 語意化 h1/h2/h3、sitemap-index.xml、robots.txt
- 優惠碼按鈕：分潤連結（target=_blank、rel="nofollow noopener"）；無分潤顯示純文字碼
- 一鍵複製優惠碼（漸進增強小 JS，不影響爬蟲）

## 待辦

- [ ] 使用者提供 GitHub token → 建 repo、推程式碼
- [ ] 接 Cloudflare Pages（見上）
- [ ] 確認新品牌分潤連結（yoxi 已死 404；其餘 9 組待確認是否續約）
- [ ] 新站上線後退役 Google Sites 舊站
- [ ] Google Search Console 提交 sitemap（https://taikeqiu.pages.dev/sitemap-index.xml）
