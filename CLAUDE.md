# 石榴放蕊（繁體中文每日讀）— 給 Claude 的專案說明

## 專案是什麼
把靈修書《石榴放蕊》（365 篇、九大主題）從簡體轉成**台灣繁體**，產出兩樣東西：
1. **PDF**：`pdf/石榴放蕊_繁體中文版_全365篇.pdf`（石榴紅版面，已定稿，**不要更動配色或版面**，除非使用者明確要求）
2. **每日閱讀網站**：`docs/`（GitHub Pages 從 `docs/` 發布）

## 使用者（Howard）
- 用台灣繁體中文溝通；**完全沒有技術背景**，每一步都要用白話解釋、一步一步帶。
- 希望 Claude 當夥伴：有更好的想法要主動提出、討論，不要什麼都說好；不清楚就先問。
- 網站給教會弟兄姊妹追求用，版權已確認沒問題。

## 資料夾
- `content/*.txt`：**唯一的內容來源**（簡體原文，已人工校對）。每行一個標記：
  `S:` 主題名＋主題經文、`T:` 篇名、`V:` 中文經文、`E:` 英文經文、`P:` 段落、`H:` 詩歌標題、`L:` 歌詞（用 `|` 分欄）。
  檔名順序就是篇號順序（01→25），篇號自動從 001 編到 365。
- `scripts/build_pdf.py`：讀 content → 簡轉繁（OpenCC `s2tw` + `FIX` 對照表修正易錯字）→ WeasyPrint 產 PDF。
- `scripts/export_data.py`：把同一份轉換結果輸出成 `build/data.json`。
- `scripts/build_web.py`：把 `web/app-body.html` + data 組成 `docs/index.html`，另產 manifest、service worker、圖示。
- `web/app-body.html`：網站全部的版面、樣式、程式（單一檔）。
- `web/firebase-config.js`：Firebase 設定，目前是 `null`（尚未申請）。
- `firestore.rules`：Firestore 安全規則（每人只能讀寫自己的 `users/{uid}`）。

## 重建
```
pip install -r requirements.txt
python3 build_all.py        # PDF + 網站
python3 build_all.py web    # 只重建網站（快）
```
改內容 → 改 `content/*.txt`；改網站 → 改 `web/app-body.html`；改完都要重建並 commit `docs/`。

## 繁體轉換注意
OpenCC 會選錯的字放在 `scripts/build_pdf.py` 的 `FIX`（例如 麵／面、鐘／鍾、乾／幹、裡／里、髮）。新增內容後要掃一遍這類字。
引號一律轉成「」『』。英文經文不轉換。

## 網站已定案的決定
- 每人從自己按「從今天開始讀」那天算第 1 天（不是全教會同一天）；365 天後循環。
- 配色四組：**石榴紅（預設）**、晴空淡藍、晨霧青綠、薰衣草灰紫；各有淺色／深色，可「跟隨手機」。
  深色模式不要用粉紅色字；淺色背景不要米色（石榴紅淺色是白底，與 PDF 一致）。
- 不要字體大小提示；「隱私說明」區塊已移除，不要加回。
- 進度保存採「方案 ③」：不登入也能讀（存在本機 localStorage）；想永久保存可用 Google 登入（Firebase Auth + Firestore，文件 `users/{uid}`：start、read（篇號→true）、palette、theme）。
  另有「進度碼」（SL1-YYYYMMDD-base64url 位元表）可備份／還原。
- 保存提醒：上方 ⚠ 未保存／✓ 已保存 標示；首次開啟歡迎卡；第一次按已讀的提示；第 7/30/100/200/300 篇與讀完主題時提醒；「以後再說」7 天不再提醒；已登入者不提醒。
  iPhone Safari 未加入主畫面時顯示加入教學（避免 Safari 7 天清資料）。
- PWA：manifest + sw.js（網頁先連網取最新，離線用快取）。改版時把 `sw.js` 的 `CACHE` 版本號加一。

## 尚未完成（下一步）
1. 推到使用者的 GitHub，開啟 GitHub Pages（Branch: main，資料夾: /docs）。
2. 帶使用者申請 Firebase：建專案 → 啟用 Authentication 的 Google 登入 → 建 Firestore → 貼上 `firestore.rules`
   → 在 Authentication「授權網域」加入 `<帳號>.github.io` → 把網頁設定貼進 `web/firebase-config.js` → 重建、commit。
3. 上線後用手機實測：登入、跨裝置同步、進度碼、加入主畫面、離線閱讀。
