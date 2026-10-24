import re
lg=open('web/logo.svg').read()
vb=re.search(r'viewBox="([^"]+)"',lg).group(1); d=re.search(r' d="([^"]+)"',lg).group(1)
SYM=f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="sl-logo" viewBox="{vb}"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></symbol></svg>'
USE='<svg aria-hidden="true"><use href="#sl-logo"/></svg>'
common,ios,andc,js=[open('scripts/components_src/'+x).read() for x in ['common.css','ios.css','and.css','engine.js']]
ih=open('scripts/components_src/ios.html').read().replace('LOGO',USE); ah=open('scripts/components_src/and.html').read().replace('LOGO',USE)
hdr='<!-- 加入主畫面教學動畫元件（由 scripts/make_a2hs.py 產生，請改 scripts/components_src/ 再重跑）。顏色用網站的配色變數，會跟著配色與深淺模式變。\n     放進網站：<style> 併入主樣式；SYMBOL（Logo 圖形定義）放一次；動畫區塊放進加入主畫面卡片；<script> 放頁面底部。 -->\n'
R='web/components/'
open(R+'a2hs-iphone.html','w').write(hdr+f'<style>\n{common}{ios}</style>\n{SYM}\n{ih}\n<script>\n{js}</script>\n')
open(R+'a2hs-android.html','w').write(hdr+f'<style>\n{common}{andc}</style>\n{SYM}\n{ah}\n<script>\n{js}</script>\n')
# preview page
P=[('r','石榴紅','#ffffff','#ffffff','#222222','#76696a','#ece4e4','#7a1f2b','#171112','#201819','#ece6e3','#a89c9a','#352a2b','#d6b06e'),
   ('b','晴空淡藍','#f5f7fb','#ffffff','#1c2533','#6b778a','#e1e7f0','#3b6ea8','#0f141c','#161d28','#e3e9f2','#95a1b3','#243042','#90b8ea'),
   ('a','晨霧青綠','#f4f8f7','#ffffff','#1e2b29','#667a76','#dfe9e6','#2f7f73','#111917','#18221f','#e2ece9','#93a6a1','#26332f','#86cdbd'),
   ('c','薰衣草灰紫','#f7f6fb','#ffffff','#24223a','#73708b','#e7e5f2','#5f5aa2','#14131c','#1c1b27','#e8e6f3','#a19eb8','#2c2a3c','#b7b2ec')]
css=''
for k,n,bg,cd,ink,mu,li,acc,dbg,dcd,dink,dmu,dli,dacc in P:
    css+=f'html[data-p="{k}"]{{--bg:{bg};--card:{cd};--ink:{ink};--muted:{mu};--line:{li};--acc:{acc};--onacc:#fff}}\n'
    css+=f'html[data-p="{k}"][data-t="d"]{{--bg:{dbg};--card:{dcd};--ink:{dink};--muted:{dmu};--line:{dli};--acc:{dacc};--onacc:{dbg}}}\n'
btns=''.join(f'<button data-pp="{k}">{n}</button>' for k,n,*_ in P)
page=f'''<!doctype html><html lang="zh-Hant-TW" data-p="r" data-t="l"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>加入主畫面動畫</title>
<style>{css}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans TC","Noto Sans CJK TC",sans-serif;padding:20px 16px 40px}}
.wrap{{max-width:720px;margin:0 auto}} h1{{font-size:21px;margin:0 0 4px}} .sub{{color:var(--muted);font-size:14px;margin:0 0 14px}}
.bar{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}} .bar button{{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}}
.bar button.on{{background:var(--acc);color:var(--onacc);border-color:var(--acc)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:18px}} .card h2{{font-size:17px;margin:0 0 12px}}
{common}{ios}{andc}</style></head><body><div class="wrap">
<h1>加入主畫面教學動畫</h1><p class="sub">iPhone（Safari）與 Android（Chrome）兩版。上方可切換配色與深淺，動畫顏色會跟著變。</p>
<div class="bar">{btns}<button data-tt="l">淺色</button><button data-tt="d">深色</button></div>
{SYM}
<div class="card"><h2>iPhone（Safari）</h2>{ih}</div>
<div class="card"><h2>Android（Chrome）</h2>{ah}</div>
</div><script>{js}
var H=document.documentElement;function mark(){{document.querySelectorAll('[data-pp]').forEach(b=>b.classList.toggle('on',b.dataset.pp===H.dataset.p));document.querySelectorAll('[data-tt]').forEach(b=>b.classList.toggle('on',b.dataset.tt===H.dataset.t))}}
document.querySelectorAll('[data-pp]').forEach(b=>b.onclick=()=>{{H.dataset.p=b.dataset.pp;mark()}});document.querySelectorAll('[data-tt]').forEach(b=>b.onclick=()=>{{H.dataset.t=b.dataset.tt;mark()}});mark();</script></body></html>'''
open('build/a2hs-preview.html','w').write(page)
print('ok')
