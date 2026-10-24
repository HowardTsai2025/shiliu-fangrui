"""把 content/ 的文字整理成網站用的資料（build/data.json），不產生 PDF。"""
import json, os
src = open('scripts/build_pdf.py', encoding='utf-8').read()
src = src[:src.index("e = html.escape")]   # 只執行讀檔與繁體轉換的部分
g = {}; exec(src, g)
lines = g['lines']; THEMES = g['THEMES']
themes = []; cur = None; art = None; n = 0
for k, v in lines:
    if k == 'S': cur = {'n': v, 'i': THEMES.index(v), 'intro': [], 'a': []}; themes.append(cur); art = None
    elif k == 'T': n += 1; art = {'no': n, 't': v, 'b': []}; cur['a'].append(art)
    else: (art['b'] if art else cur['intro']).append([k, v])
os.makedirs('build', exist_ok=True)
json.dump(themes, open('build/data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('data.json:', n, '篇')
