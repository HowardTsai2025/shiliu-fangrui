"""產生 GitHub Pages 網站到 docs/。"""
import json,re,os,shutil
data=open('build/data.json').read().replace('</','<\\/')
body=open('web/app-body.html').read().replace('__DATA__',data)
# 加到主畫面動畫：從 scripts/components_src/ 組進來
C='scripts/components_src/'; rd=lambda x: open(C+x,encoding='utf-8').read()
_lg=open('web/logo.svg').read(); _vb=re.search(r'viewBox="([^"]+)"',_lg).group(1); _d=re.search(r' d="([^"]+)"',_lg).group(1)
SYM=f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="sl-logo" viewBox="{_vb}"><path fill="currentColor" fill-rule="evenodd" d="{_d}"/></symbol></svg>'
USE='<svg aria-hidden="true"><use href="#sl-logo"/></svg>'
oneline=lambda x: re.sub(r'\s*\n\s*',' ',rd(x).replace('LOGO',USE)).replace('`','\\`')
body=(body.replace('/*__A2HS_CSS__*/',rd('common.css')+rd('ios.css')+rd('and.css'))
          .replace('__A2HS_SYMBOL__',SYM).replace('/*__A2HS_ENGINE__*/',rd('engine.js'))
          .replace('__A2HS_IOS__',oneline('ios.html')).replace('__A2HS_AND__',oneline('and.html')))
os.makedirs('docs',exist_ok=True)
# artifact preview (body only)
open('build/preview-artifact.html','w').write(body)  # 給 Claude 網頁預覽用（只有內文）
title_and_rest=body
head_extra='''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#ffffff">
<meta name="description" content="《石榴放蕊》繁體中文每日靈修，一天一篇，共 365 篇。">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="石榴放蕊">
<script src="firebase-config.js"></script>
<script>if('serviceWorker' in navigator){addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))}</script>'''
# move <title>,<meta claude>,<link>,<style> into head
m=re.match(r'(.*?</style>\n<script>.*?</script>)(.*)',body,re.S)
headpart,rest=m.group(1),m.group(2)
headpart=headpart.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
doc=f'<!doctype html>\n<html lang="zh-Hant-TW">\n<head>\n{head_extra}\n{headpart}\n</head>\n<body>{rest}\n</body>\n</html>\n'
open('docs/index.html','w').write(doc)
for f in ['icon-192.png','icon-512.png','icon-maskable.png','apple-touch-icon.png','favicon.svg']: shutil.copy('web/icons/'+f,'docs/'+f)
json.dump({"name":"石榴放蕊 每日讀","short_name":"石榴放蕊","lang":"zh-Hant-TW","start_url":"./","scope":"./","display":"standalone",
 "background_color":"#ffffff","theme_color":"#ffffff",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},
          {"src":"icon-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open('docs/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
open('docs/sw.js','w').write('''// 離線快取：網頁先試著連網取得最新版，沒網路時用手機裡存的版本
const CACHE='shiliu-v4';
const CORE=['./','index.html','manifest.webmanifest','firebase-config.js','icon-192.png','icon-512.png','apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET') return;
  if(u.origin===location.origin){
    e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request).then(r=>r||caches.match('index.html'))));
  } else if(/fonts\\.(googleapis|gstatic)\\.com/.test(u.host)){
    e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{const c=res.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return res})));
  }
});
''')
shutil.copy('web/firebase-config.js','docs/firebase-config.js')
if False:
    open('docs/firebase-config.js','w').write('''// Firebase 設定（用來讓大家登入 Google 保存進度）
// 申請好 Firebase 之後，把下面的 null 換成 Firebase 給你的設定即可。
// 還沒設定時，網站照常可以閱讀，只是不會出現「用 Google 登入」按鈕，大家用「進度碼」備份。
window.FIREBASE_CONFIG = null;
''')
open('firestore.rules','w').write('''rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 每個人只能讀寫自己的進度
    match /users/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
''')
open('docs/.nojekyll','w').write('')
print('built', os.path.getsize('docs/index.html'))
