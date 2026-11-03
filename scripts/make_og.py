"""產生 LINE／Facebook 分享預覽圖 web/icons/og-image.png（1200×630，石榴紅底＋白色 Logo）：python3 scripts/make_og.py
（需要 playwright + chromium；換 Logo 時跟著重產。標題文字 LINE 會自己顯示在圖下方，所以圖上只放 Logo）"""
import asyncio
from playwright.async_api import async_playwright
svg = open('web/logo.svg', encoding='utf-8').read().replace('<svg ', '<svg width="400" height="400" ')
html = ('<html><body style="margin:0"><div style="width:1200px;height:630px;background:#7a1f2b;color:#fff;'
        f'display:flex;align-items:center;justify-content:center">{svg}</div></body></html>')
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        await pg.set_content(html); await pg.screenshot(path='web/icons/og-image.png'); await b.close()
    print('✓ web/icons/og-image.png')
asyncio.run(main())
