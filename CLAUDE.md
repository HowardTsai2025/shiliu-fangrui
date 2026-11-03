# 石榴放蕊（繁體中文每日讀）— 給 Claude 的專案說明

## 專案是什麼
把靈修書《石榴放蕊》（365 篇、九大主題）從簡體轉成**台灣繁體**，產出兩樣東西：
1. **PDF**：`pdf/石榴放蕊_繁體中文版_全365篇.pdf`（石榴紅版面，已定稿，**不要更動配色或版面**，除非使用者明確要求；封面標題上方有白色 Logo，經使用者同意加入）
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
- `web/logo.svg`：Logo「晨光石榴」（使用者用 Nano Banana 產生的原圖描成向量，**照原圖，不要自行重新設計**）。顏色用 currentColor，網站標題列會跟配色變色。
- `scripts/make_icons.py`：用 logo.svg 產生主畫面圖示（石榴紅底＋白果，使用者選定）、maskable、apple-touch、PDF 封面用白色 Logo（web/icons/cover-logo.png）。需要 playwright，只有換 Logo 時才要跑（`python3 build_all.py icons`）；產出的圖示都已 commit。
- `web/firebase-config.js`：Firebase 設定，目前是 `null`（尚未申請）。
- `firestore.rules`：Firestore 安全規則（每人只能讀寫自己的 `users/{uid}`）。

## 重建
```
pip install -r requirements.txt
python3 build_all.py        # PDF + 網站
python3 build_all.py web    # 只重建網站（快）
python3 build_all.py icons  # 換了 web/logo.svg 才需要（要 playwright + chromium）
```
改內容 → 改 `content/*.txt`；改網站 → 改 `web/app-body.html`；改完都要重建並 commit `docs/`。

## 繁體轉換注意
OpenCC 會選錯的字放在 `scripts/build_pdf.py` 的 `FIX`（例如 麵／面、鐘／鍾、乾／幹、裡／里、髮）。新增內容後要掃一遍這類字。
引號一律轉成「」『』。英文經文不轉換。

## 網站已定案的決定
- 每人從自己按「從今天開始讀」那天算第 1 天（不是全教會同一天）；365 天後循環。
- 配色五組：**石榴紅（預設）**、晴空淡藍、晨霧青綠、薰衣草灰紫、向日葵黃（活潑款，白底＋亮黃按鈕配深色字；文字強調色用 `--acct` 較深的金色才看得清楚）；各有淺色／深色，可「跟隨手機」。
  深色模式不要用粉紅色字；淺色背景不要米色（石榴紅淺色是白底，與 PDF 一致）。
- 不要字體大小提示；「隱私說明」區塊已移除，不要加回。
- 進度保存採「方案 ③」：不登入也能讀（存在本機 localStorage）；想永久保存可用 Google 登入（Firebase Auth + Firestore，文件 `users/{uid}`：start、read（篇號→true）、palette、theme）。
  另有「進度碼」（SL1-YYYYMMDD-base64url 位元表）可備份／還原。
- 保存提醒：上方 ⚠ 未保存／✓ 已保存 標示；首次開啟歡迎卡；第一次按已讀的提示；第 7/30/100/200/300 篇與讀完主題時提醒；「以後再說」7 天不再提醒；已登入者不提醒。
- 「把它加到手機主畫面」卡片（今日頁上方＋設定頁）：自動判斷手機——iPhone 只顯示 iPhone 動畫；Android 若 Chrome 提供安裝事件（beforeinstallprompt）就顯示「📲 一鍵加到主畫面」按鈕，動畫收在「按了沒反應？看圖解步驟」裡，否則直接顯示 Android 動畫；在 LINE 等 App 內建瀏覽器開啟時，改提示用 Safari／Chrome 打開（LINE 用網址參數 openExternalBrowser=1）。已是主畫面 App 時不顯示。「知道了，先不用」隱藏 30 天。
  動畫原始檔在 `scripts/components_src/`（共用 common.css、engine.js），`build_web.py` 會組進網站；`scripts/make_a2hs.py` 另產獨立元件與預覽。
  動畫規則：播一次，播完顯示重新播放；同一次開啟網頁內播過就不再自動重播。
- 標題列：Logo＋「石榴放蕊」＋保存狀態。分頁（今日／目錄／搜尋／設定）有圖示＋字：手機（寬 ≤700）放在螢幕最下方像 App 的分頁列（使用者選定），電腦／平板放在標題列右側。
- 字型：內文、主題標題、文章標題都用思源宋體（Noto Serif TC），標題用粗體；不提供字型切換（使用者決定）。
- 從搜尋或目錄點進文章，上方有「‹ 回到搜尋結果／回到目錄」，回去時保留捲動位置。
- 輸入框字級一律 ≥16px（小於 16px 時 iPhone Safari 點輸入框會自動放大畫面、不縮回，畫面右邊被切掉）。不要用關閉縮放的方式解決（長輩需要能手動放大）。
  另外 `.panel` 是 grid，要保持 `grid-template-columns:minmax(0,1fr)`：iPhone 的輸入框預設很寬，少了這個會把卡片內容撐出螢幕右邊（Chromium 測不出來，測試時可把 input 的 size 設成 80 模擬）。
- PWA：manifest + sw.js（網頁先連網取最新，離線用快取）。改版時把 `sw.js` 的 `CACHE` 版本號加一。

## 尚未完成（下一步）
專案已推上 GitHub：`HowardTsai2025/shiliu-fangrui`（public，分支 `main`）。git 身分：`HowardTsai2025 <276nndy9st@privaterelay.appleid.com>`（使用者提供；舊提交作者已改寫成這個）。
1. ~~設定 git 身分~~ ✅
2. ~~GitHub Pages~~ ✅ 已開啟（main /docs）：`https://howardtsai2025.github.io/shiliu-fangrui/`（雲端環境連不到這個網址，要請使用者用手機看）。
3. **上線後手機實測**：iPhone Safari 加入主畫面、Android Chrome「📲 一鍵加到主畫面」按鈕是否出現（需要正式網址＋service worker）、
   從 LINE 打開時「用 Safari／Chrome 打開」按鈕（網址參數 `openExternalBrowser=1`）是否有效、離線閱讀、進度碼。
4. **Firebase（Google 登入保存進度）**：建專案 → Authentication 啟用 Google → 建 Firestore（選離台灣近的區域，如 asia-east1）→ 貼上 `firestore.rules`
   → Authentication「授權網域」加入 `<帳號>.github.io` → 把網頁應用程式設定貼進 `web/firebase-config.js` → `sw.js` 的 CACHE 版本加一 → 重建、commit、push → 兩支手機實測同步。
5. **之後可考慮**（使用者已知道，尚未決定）：Email 連結登入（免費方案每天只能寄 5 封，需綁卡升級 Blaze）、LINE 登入（需 Blaze + Identity Platform OIDC + LINE Developers）。Apple 登入不建議（年費）。

## 每次改完網站
改 `web/app-body.html` 或 `scripts/components_src/` → `python3 build_all.py web` → 用手機寬度檢查 → `sw.js` 的 CACHE 版本加一（已上線後）→ commit、push。
