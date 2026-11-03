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
- `web/firebase-config.js`：Firebase 設定（專案 ID `shi-liu-fang-rui`，Spark 免費方案；Firestore 在 asia-east1）。改成 `null` 就關掉 Google 登入。
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
- 字體大小（小／中／大／特大＝16/18/20/22）：**整個網站的字都跟著縮放**（CSS 變數 `--k`＝字體大小÷18，app-body 樣式裡所有 `font-size` 都寫成 `calc(Npx*var(--k))`；新增樣式也要這樣寫）。
  **按鈕、分頁、選項的字絕對不能換行**（使用者要求；`white-space:nowrap`，放不下時整顆按鈕換行）。設定頁字體大小下方有預覽文字；按了畫面停在原處。
  測試：iPhone／iPhone SE(320)／Android／iPad／Android 平板／電腦 × 4 種字級，檢查超出畫面與按鈕字換行（用 Range 算行數，別用高度判斷）。
- 用詞依裝置自動判斷：`DEV`（手機／平板／電腦）、`THIS_DEV`（這支手機／這台平板／這台電腦）；固定文字用「換手機、平板或電腦」；深淺選項是「跟隨系統」。不要寫死「手機」。
- 進度保存採「方案 ③」：不登入也能讀（存在本機 localStorage）；想永久保存可用 Google 登入（Firebase Auth + Firestore，文件 `users/{uid}`：start、read（篇號→true）、palette、theme）。
  另有「進度碼」（SL1-YYYYMMDD-base64url 位元表）可備份／還原。
- 已登入時，任何地方都不要再出現「用 Google 登入保存」按鈕或「進度只存在這支手機」（歡迎卡改顯示「✓ 已用 Google 帳號登入」）。
- 文章上方標籤「今日進度」、按鈕「回到今日進度（第 N 篇）」（使用者指定，不用「今天」）；「從今天開始讀」「今天是第 N 天」維持「今天」。
- 使用者精簡過的文字（不要加回）：歡迎卡標題「歡迎使用《石榴放蕊》」、內文只有「一天一篇，共 365 篇。」；設定頁卡片標題「閱讀進度」、不顯示「今天是第 N 天…」說明、不顯示「已讀紀錄」標籤；目錄上方只有「已讀 N / 365 篇。」。
- 開始日期顯示 yyyy/MM/dd（`.datebox`：自己顯示文字，透明的系統日期欄位蓋在上面；系統欄位的格式跟著手機語系改不了）。
- iPhone／iPad：Safari 和主畫面 App 的儲存是分開的（登入、進度都不共用；Apple 的限制，Android 沒有這問題）。所以在 iPhone／iPad 的 Safari（`A2_FIRST()`）：
  今日頁「加到主畫面」卡片放在歡迎卡上面；歡迎卡不放登入按鈕，改顯示「📱建議把網站先加到主畫面，從主畫面打開後再登入，這樣只要登入一次。」（使用者指定文字）；
  設定頁登入按鈕保留並加註「主畫面 App 和 Safari 是分開的…要再登入一次」。按「知道了，先不用」後恢復一般流程。**讀到第幾篇的保存提醒不要動**（使用者決定：不想加主畫面的人照常登入）。
- 加入主畫面卡片（今日頁、設定頁）標題「加入主畫面變成 App！」，標題下不放說明文字（使用者指定）。
- 名稱一律「石榴放蕊」（動畫、manifest 的 name 都不加「每日讀」）。
- 登入失敗會跳提示並顯示錯誤代碼（使用者自己關掉視窗則不提示）；請使用者截圖錯誤代碼來除錯。
- 保存提醒：上方 ⚠ 未保存／✓ 已保存 標示；首次開啟歡迎卡；第一次按已讀的提示；第 7/30/100/200/300 篇與讀完主題時提醒；「以後再說」7 天不再提醒；已登入者不提醒。
- 「把它加到手機主畫面」卡片（今日頁上方＋設定頁）：自動判斷手機——iPhone 只顯示 iPhone 動畫；Android 若 Chrome 提供安裝事件（beforeinstallprompt）就顯示「📲 一鍵加到主畫面」按鈕，動畫收在「按了沒反應？看圖解步驟」裡，否則直接顯示 Android 動畫；在 LINE 等 App 內建瀏覽器開啟時，改提示用 Safari／Chrome 打開（LINE 用網址參數 openExternalBrowser=1）。已是主畫面 App 時不顯示。「知道了，先不用」隱藏 30 天。
  動畫原始檔在 `scripts/components_src/`（共用 common.css、engine.js），`build_web.py` 會組進網站；`scripts/make_a2hs.py` 另產獨立元件與預覽。
  動畫規則：播一次，播完顯示重新播放；同一次開啟網頁內播過就不再自動重播。
  平板：iPad 有專用動畫 `ipad.html/ipad.css`（上方工具列右邊的分享鈕 → 分享選單 → 加入主畫面 → 新增；**依 iPadOS 介面推測畫的，尚未用真 iPad 對照**，有人回報再修）；Android 平板用同一套 Chrome 動畫加 `.tab`（平板外框）。
  動畫元件的 class 不要和網站樣式撞名（曾撞到 `.pop`、`.dim`、`.list`）；`.a2hs` 有 `isolation:isolate`，標題列 z-index 20，避免動畫蓋到下方分頁列（Android 曾發生）。
- 標題列：Logo＋「石榴放蕊」＋保存狀態。分頁（今日／目錄／搜尋／設定）有圖示＋字：手機（寬 ≤700）放在螢幕最下方像 App 的分頁列（使用者選定），電腦／平板放在標題列右側。
- 字型：內文、主題標題、文章標題都用思源宋體（Noto Serif TC），標題用粗體；不提供字型切換（使用者決定）。
- 從搜尋或目錄點進文章，上方有「‹ 回到搜尋結果／回到目錄」，回去時保留捲動位置。
- iPhone／iPad 上不是 Safari 時（CriOS=Chrome、FxiOS、EdgiOS），加入主畫面教學裡的「Safari」自動換成實際瀏覽器名稱（brFix）。iPad Chrome 的分享鈕也在右上，動畫相符；iPhone Chrome 有專用動畫（components_src/ioscr.html，v16，依使用者截圖：網址列在下方、分享鈕在網址列右邊、下面一排 ← → ＋ 分頁 ⋯；流程 分享→加入主畫面→新增→完成）。
- LINE 等 App 內建瀏覽器沒有「加入主畫面」，所以不顯示動畫，改顯示「用 Safari／Chrome 打開」按鈕＋「打開後就會出現圖解步驟」。
- Android 平板動畫第 2 步寫「有些平板寫…」。
- 分頁列任何按鈕連按兩下（450ms 內）→ 平滑捲回頁首（不重畫頁面）；點標題「石榴放蕊」或 Logo → 回到今日進度並捲到最上面（像回首頁）。
- iPhone 輸入框收起鍵盤後，固定在下方的分頁列可能漂浮在畫面中間（短頁面最明顯，例如搜尋頁）：focusout 與 visualViewport resize 時呼叫 settle() 把捲動位置推回合法範圍。v14 加入，待使用者 iPhone 實測。
- 輸入框字級一律 ≥16px（小於 16px 時 iPhone Safari 點輸入框會自動放大畫面、不縮回，畫面右邊被切掉）。不要用關閉縮放的方式解決（長輩需要能手動放大）。
  另外 `.panel` 是 grid，要保持 `grid-template-columns:minmax(0,1fr)`：iPhone 的輸入框預設很寬，少了這個會把卡片內容撐出螢幕右邊（Chromium 測不出來，測試時可把 input 的 size 設成 80 模擬）。
- 分享預覽（LINE 等）：`build_web.py` 的 description／og 標籤，文字是使用者指定的經文「我們清晨起來往葡萄園去，看看葡萄發芽開花沒有，石榴放蕊沒有；我在那裏要將我的愛情給你。」（歌七12），不要改；
  預覽圖 `web/icons/og-image.png`（1200×630 石榴紅底白 Logo，`scripts/make_og.py` 產生，換 Logo 時重產）。LINE 會快取預覽，改了可能要過一陣子才更新。
- PWA：manifest + sw.js（網頁先連網取最新，fetch 用 `cache:'no-cache'` 避開 GitHub Pages 的 10 分鐘暫存；離線用快取）。
- 版本號：`scripts/build_web.py` 的 `VERSION`，同時是 sw.js 快取名稱，也顯示在設定頁最下面「版本 vN」（請使用者看這個確認手機拿到的是不是新版）。

## 交接紀錄（2026-11-03，Claude Code 雲端 → 回到 Claude 聊天）
- 目前線上版本：**v13**，網站程式最後一次修改是提交 `632093d`；交接包的 git 紀錄與當時 GitHub `main` 完全相同。網站 = `docs/`，與線上完全一致。
- 這段期間（v5→v13）做的事：iPhone 輸入框放大／超出修正、sw.js no-cache 與版本號、Google 登入上線並實測、字體大小整站縮放、
  用詞依裝置判斷、iPad／Android 平板動畫、分享預覽（歌七12＋og-image）、Android 動畫蓋分頁列修正、登入後隱藏登入按鈕、
  iPhone／iPad Safari 先引導加入主畫面、多處文字精簡（細節都已寫進上面「網站已定案的決定」）。
- 在聊天裡繼續修改時：**每次改完請照常 `git commit`**（不用 push），讓紀錄接在交接包原本的紀錄後面；版本號 `VERSION` 照常加一。
  預覽可用 `build/preview-artifact.html`（`python3 build_all.py web` 會產生）。
- **這段期間不要在 GitHub 網站上直接改檔案**，回來 deploy 時才能直接接上、不會衝突。
- 回來 deploy 時：把整個資料夾（含 `.git`）打包上傳，Claude 會比對 GitHub `main` 的最新提交，確認聊天裡的紀錄是接在它後面，再推上 GitHub，請使用者看設定頁版本號確認。
- 注意：`scripts/make_og.py`、`make_icons.py` 需要 Python 版 playwright（只有換 Logo 才要跑）。
- **聊天裡完成 v14～v16（2026-11-03，接在 GitHub `main` 的 `e4b1c10` 後面，共 3＋1 筆提交，尚未 push）**：
  v14 分頁列連按兩下回頁首、點標題／Logo 回今日進度、iPhone 收鍵盤後分頁列漂浮修正（settle）；
  v15 iPhone／iPad 非 Safari 瀏覽器教學改寫實際名稱、LINE 內提示、Android 平板用詞；
  v16 iPhone Chrome 專用動畫（components_src/ioscr.html）。
  回到 Claude Code：確認 `origin/main` 仍是 `e4b1c10` → 直接 `git push` → 請使用者看設定頁版本號是否為 v16。
  上線後待使用者實測：iPhone 搜尋頁收鍵盤後分頁列是否回到底部、iPhone Chrome 動畫、連按兩下回頁首、點標題回今日。

## 尚未完成（下一步）
專案已推上 GitHub：`HowardTsai2025/shiliu-fangrui`（public，分支 `main`）。git 身分：`HowardTsai2025 <276nndy9st@privaterelay.appleid.com>`（使用者提供；舊提交作者已改寫成這個）。
1. ~~設定 git 身分~~ ✅
2. ~~GitHub Pages~~ ✅ 已開啟（main /docs）：`https://howardtsai2025.github.io/shiliu-fangrui/`（雲端環境連不到這個網址，要請使用者用手機看）。
3. **上線後手機實測**：iPhone Safari 加入主畫面、Android Chrome「📲 一鍵加到主畫面」按鈕是否出現（需要正式網址＋service worker）、
   從 LINE 打開時「用 Safari／Chrome 打開」按鈕（網址參數 `openExternalBrowser=1`）是否有效、離線閱讀、進度碼。
   已測：✅ 進度碼產生／還原（iPhone）、✅ iPhone 設定頁輸入框不再放大／超出（v5 確認）、✅ 從 LINE 打開、✅ 飛航模式離線閱讀、✅ iPhone 加入主畫面。待測：Android（使用者之後找人確認）。
4. **Firebase（Google 登入保存進度）**（v6 已上線：Google 登入已啟用、授權網域已加 howardtsai2025.github.io、Firestore 建在 asia-east1、規則已發布；✅ 已實測：iPhone Safari、iPhone 主畫面 App、電腦都能順利 Google 登入；✅ 跨裝置同步（手機↔電腦）也確認成功）：建專案 → Authentication 啟用 Google → 建 Firestore（選離台灣近的區域，如 asia-east1）→ 貼上 `firestore.rules`
   → Authentication「授權網域」加入 `<帳號>.github.io` → 把網頁應用程式設定貼進 `web/firebase-config.js` → `build_web.py` 的 VERSION 加一 → 重建、commit、push → 兩支手機實測同步。
4.5 **試用期**：使用者正把網址發給 2～3 位弟兄姊妹（含 Android、長輩）試用一週，收集意見（看不懂的地方、字級、顏色、怪問題截圖），修完再發給全教會。
5. **之後可考慮**（使用者已知道，尚未決定）：Email 連結登入（免費方案每天只能寄 5 封，需綁卡升級 Blaze）、LINE 登入（需 Blaze + Identity Platform OIDC + LINE Developers）。Apple 登入不建議（年費）。

## 每次改完網站
改 `web/app-body.html` 或 `scripts/components_src/` → `python3 build_all.py web` → 用手機寬度檢查 → `scripts/build_web.py` 的 `VERSION` 加一 → commit、push → 請使用者看設定頁最下面的版本號確認。
