"""用 web/logo.svg 產生所有圖示：python3 scripts/make_icons.py
（需要 playwright + chromium）主畫面圖示：石榴紅底＋白色石榴（使用者選定 A 款）"""
import asyncio, re
from playwright.async_api import async_playwright
RED, WHITE = '#7a1f2b', '#ffffff'
svg = open('web/logo.svg', encoding='utf-8').read()
def page(size, bg, fg, logo_ratio, radius=0):
    s = svg.replace('<svg ', f'<svg width="{int(size*logo_ratio)}" height="{int(size*logo_ratio)}" ')
    return (f'<html><body style="margin:0;background:transparent"><div style="width:{size}px;height:{size}px;'
            f'background:{bg};border-radius:{radius}px;color:{fg};display:flex;align-items:center;justify-content:center">{s}</div></body></html>')
JOBS = [  # 檔名, 尺寸, 底色, 圖色, Logo 佔比, 圓角
    ('web/icons/icon-192.png', 192, RED, WHITE, .70, 192*.18),
    ('web/icons/icon-512.png', 512, RED, WHITE, .70, 512*.18),
    ('web/icons/apple-touch-icon.png', 180, RED, WHITE, .70, 0),   # iPhone 會自己切圓角
    ('web/icons/icon-maskable.png', 512, RED, WHITE, .56, 0),      # Android 會切成各種形狀，Logo 要留在安全區
    ('web/icons/cover-logo.png', 1200, 'transparent', WHITE, 1, 0),    # PDF 封面用（白色）
]
async def main():
    import os; os.makedirs('build', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for path, size, bg, fg, r, rad in JOBS:
            pg = await b.new_page(viewport={'width': size, 'height': size})
            await pg.set_content(page(size, bg, fg, r, rad))
            await pg.screenshot(path=path, omit_background=True)
            await pg.close(); print('✓', path)
        await b.close()
asyncio.run(main())
