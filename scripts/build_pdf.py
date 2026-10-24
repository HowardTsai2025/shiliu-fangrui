import glob, html, re, os, opencc
from weasyprint import HTML

cc = opencc.OpenCC('s2tw')
FIX = {'撫發':'撫髮','一點面':'一點麵','僅有的面':'僅有的麵','面粉':'麵粉','漂鍾':'漂鐘','把鍾':'把鐘','沒有幹過':'沒有乾過','不準留':'不准留','面缸':'麵缸','面包':'麵包','壇內的面':'罈內的麵','罈內的面':'罈內的麵','只準吃':'只准吃','相信鍾':'相信鐘','鍾鑄好':'鐘鑄好','敲那鍾':'敲那鐘','云霧':'雲霧','海里':'海裡','米里':'米裡','會里':'會裡'}
THEMES = ['早起','讀經','禱告','交通','信心','了結已往','奉獻','對付罪','對付世界']
NUMS = '一二三四五六七八九'

def tw(s):
    s = cc.convert(s).replace('喂', '餵')
    for a, b in FIX.items(): s = s.replace(a, b)
    s = s.replace('‘', '「').replace('’', '」').replace('“', '『').replace('”', '』')
    return s

lines = []
for f in sorted(glob.glob('content/*.txt')):
    for l in open(f, encoding='utf-8'):
        l = l.rstrip('\n')
        if l.strip():
            k, v = l.split(': ', 1) if ': ' in l else (l[:1], l[3:])
            lines.append((k, v if k == 'E' else tw(v)))

# Group into themes -> articles
themes = []; cur = None; art = None; n = 0
for k, v in lines:
    if k == 'S':
        cur = {'name': v, 'intro': [], 'arts': []}; themes.append(cur); art = None
    elif k == 'T':
        n += 1; art = {'no': n, 'title': v, 'body': []}; cur['arts'].append(art)
    else:
        (art['body'] if art else cur['intro']).append((k, v))

e = html.escape
def split_ref(v, zh=True):
    m = re.search(r'[（(]([^（）()]+)[）)]\s*$', v)
    if not m: return e(v), ''
    return e(v[:m.start()].rstrip()), e(m.group(1).strip())

def body_html(items, theme=False):
    out = []; i = 0
    while i < len(items):
        k, v = items[i]
        if k == 'V' and theme:
            zt, zr = split_ref(v)
            h = f'<div class="zh">{zt}</div><div class="ref">{zr}</div>'
            if i + 1 < len(items) and items[i+1][0] == 'E':
                et, er = split_ref(items[i+1][1]); i += 1
                h += f'<div class="en">{et}</div><div class="ref en-ref">{er}</div>'
            out.append(f'<div class="verse">{h}</div>')
        elif k == 'V':
            en = ''
            if i + 1 < len(items) and items[i+1][0] == 'E':
                en = f'<div class="en">{e(items[i+1][1])}</div>'; i += 1
            out.append(f'<div class="verse"><div class="zh">{e(v)}</div>{en}</div>')
        elif k == 'E':
            out.append(f'<div class="verse"><div class="en">{e(v)}</div></div>')
        elif k == 'P':
            out.append(f'<p>{e(v)}</p>')
        elif k in 'HL':
            block = []
            if k == 'H':
                block.append(f'<div class="htitle">詩歌　{e(v)}</div>'); i += 1
            while i < len(items) and items[i][0] == 'L':
                parts = [e(p) for p in items[i][1].split('|')]
                block.append('<div class="lyric">' + ''.join(f'<span>{p}</span>' for p in parts) + '</div>')
                i += 1
            out.append('<div class="hymn">' + ''.join(block) + '</div>')
            continue
        i += 1
    return '\n'.join(out)

parts = []
toc = []
for ti, th in enumerate(themes):
    idx = THEMES.index(th['name'])
    a0, a1 = th['arts'][0]['no'], th['arts'][-1]['no']
    label = f'（{NUMS[idx]}）{th["name"]}'
    toc.append(f'<div class="toc-theme"><a href="#t{idx}">{label}<span class="rng">第 {a0:03d}–{a1:03d} 篇</span></a></div>')
    for a in th['arts']:
        toc.append(f'<div class="toc-item"><a href="#a{a["no"]}"><span class="tn">{a["no"]:03d}</span>{e(a["title"])}</a></div>')
    parts.append(f'''<section class="theme" id="t{idx}">
<div class="theme-no">第{NUMS[idx]}主題</div>
<h1 class="theme-name">{th["name"]}</h1>
<div class="theme-range">第 {a0:03d} 篇 – 第 {a1:03d} 篇　共 {a1-a0+1} 篇</div>
<div class="theme-intro">{body_html(th["intro"], theme=True)}</div>
</section>''')
    for a in th['arts']:
        parts.append(f'''<article id="a{a["no"]}" data-theme="{label}">
<header><div class="meta"><span class="num">第 {a["no"]:03d} 篇</span><span class="tag">{label}</span></div>
<h2 data-no="{a["no"]:03d}">{e(a["title"])}</h2></header>
{body_html(a["body"])}
</article>''')

total = sum(len(t['arts']) for t in themes)
cover_logo = 'cover-logo.png'  # 由 scripts/make_icons.py 產生（build/ 內）
doc = f'''<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><title>石榴放蕊</title>
<style>
@page {{ size: A4; margin: 22mm 20mm 22mm 20mm;
  @top-left {{ content: string(theme); font: 9pt "Noto Sans CJK TC"; color:#8a6d3b; }}
  @top-right {{ content: string(art); font: 9pt "Noto Sans CJK TC"; color:#999; }}
  @bottom-center {{ content: counter(page); font: 9pt "Noto Sans CJK TC"; color:#888; }} }}
@page cover {{ margin:0; @top-left{{content:none}} @top-right{{content:none}} @bottom-center{{content:none}} }}
@page front {{ @top-left{{content:none}} @top-right{{content:none}} @bottom-center{{content:none}} }}
@page themep {{ @top-left{{content:none}} @top-right{{content:none}} }}
body {{ font-family: "Noto Serif CJK TC", serif; font-size: 11.5pt; line-height: 1.85; color:#222; }}
.cover {{ page: cover; height: 297mm; background:#7a1f2b; color:#fff; display:flex; flex-direction:column;
  justify-content:center; align-items:center; text-align:center; break-after: page; }}
.cover h1 {{ font-size: 54pt; letter-spacing: .3em; margin:0 0 6mm 0.3em; font-weight:700; }}
.cover .sub {{ font: 14pt "Noto Sans CJK TC"; letter-spacing:.2em; opacity:.85; }}
.cover .logo {{ width: 34mm; height: 34mm; display:block; margin: 0 auto 12mm; }}
.cover .line {{ width: 40mm; border-top:1px solid rgba(255,255,255,.6); margin: 10mm auto; }}
.toc {{ page: front; break-after: page; }}
.toc h1 {{ font: 700 20pt "Noto Sans CJK TC"; color:#7a1f2b; border-bottom:2px solid #7a1f2b; padding-bottom:2mm; }}
.toc a {{ color:inherit; text-decoration:none; }}
.toc-theme {{ font: 700 12.5pt "Noto Sans CJK TC"; color:#7a1f2b; margin: 5mm 0 1.5mm; }}
.toc-theme .rng {{ font-weight:400; font-size:9.5pt; color:#999; margin-left:4mm; }}
.toc-item {{ font-size: 10.5pt; line-height:1.7; padding-left: 4mm; }}
.toc-item a::after {{ content: leader('·') target-counter(attr(href), page); color:#888; }}
.toc-item .tn {{ font-family:"Noto Sans CJK TC"; color:#b08a4a; display:inline-block; width:11mm; }}
.theme {{ page: themep; break-before: page; break-after: page; padding-top: 55mm; text-align:center; }}
.theme-no {{ font: 14pt "Noto Sans CJK TC"; color:#b08a4a; letter-spacing:.3em; }}
.theme-name {{ string-set: theme "（" content() "）"; font: 700 40pt "Noto Sans CJK TC"; color:#7a1f2b; letter-spacing:.25em; margin: 4mm 0 4mm .25em; }}
.theme-range {{ font: 11pt "Noto Sans CJK TC"; color:#888; margin-bottom: 18mm; }}
.theme-intro {{ max-width: 135mm; margin: 0 auto; text-align:left; }}
.theme .ref {{ font: 10.5pt "Noto Sans CJK TC"; color:#8a6d3b; margin: 1.5mm 0 3mm; letter-spacing:.05em; }}
.theme .en-ref {{ font: italic 9.5pt "Times New Roman", "Liberation Serif", serif; color:#8a8a8a; margin: 1mm 0 0; letter-spacing:0; }}
.theme .verse {{ border:none; background:#faf6ee; text-align:center; padding:6mm 8mm; }}
article {{ margin-bottom: 9mm; }}
article header {{ break-after: avoid; break-inside: avoid; page-break-inside: avoid; border-top: 2px solid #7a1f2b; padding-top: 2.5mm; margin-bottom: 3mm; }}
.meta {{ font: 9.5pt "Noto Sans CJK TC"; display:flex; justify-content:space-between; }}
.num {{ background:#7a1f2b; color:#fff; padding: .3mm 2.5mm; border-radius: 1mm; font-weight:700; letter-spacing:.05em; }}
.tag {{ color:#b08a4a; }}
h2 {{ string-set: art "第 " attr(data-no) " 篇・" content(); font: 700 17pt "Noto Sans CJK TC"; color:#222; margin: 2mm 0 0; line-height:1.4; }}
header + .verse {{ break-before: avoid; }}
.verse {{ background:#f7f3ea; border-left: 3px solid #b08a4a; padding: 2.5mm 4mm; margin: 3mm 0; break-inside: avoid; }}
.verse .zh {{ font-weight:600; color:#4a3b22; }}
.verse .en {{ font-family: "Times New Roman", "Liberation Serif", serif; font-style: italic; font-size: 10pt; color:#6b6b6b; line-height:1.5; margin-top:1mm; }}
p {{ text-indent: 2em; margin: 0 0 2.2mm; text-align: justify; }}
.hymn {{ margin: 4mm 0 4mm 0; padding: 2.5mm 5mm; border: 1px dashed #c9b48a; border-radius: 2mm; break-inside: avoid; }}
.htitle {{ font: 700 10.5pt "Noto Sans CJK TC"; color:#8a6d3b; margin-bottom: 1mm; }}
.lyric {{ font-size: 10.5pt; line-height: 1.75; }}
.lyric span {{ display:inline-block; min-width: 46mm; margin-right: 4mm; }}
.lyric span:empty {{ min-width: 6mm; }}
</style></head><body>
<div class="cover"><div><img class="logo" src="{cover_logo}" alt=""><h1>石榴放蕊</h1><div class="line"></div>
<div class="sub">繁體中文版</div><div class="sub" style="margin-top:4mm;font-size:11pt">九大主題・{total} 篇</div></div></div>
<div class="toc"><h1>目錄</h1>{''.join(toc)}</div>
{''.join(parts)}
</body></html>'''
# number in running header
doc = re.sub(r'<article id="a(\d+)"', lambda m: f'<article id="a{m.group(1)}"', doc)
doc = re.sub(r'<h2>', '<h2>', doc)
os.makedirs('build',exist_ok=True); open('build/book.html', 'w', encoding='utf-8').write(doc)
HTML('build/book.html').write_pdf('pdf/石榴放蕊_繁體中文版_全365篇.pdf')
print('articles', total, [ (t['name'], len(t['arts'])) for t in themes])
