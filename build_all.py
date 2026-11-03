"""一次重建全部：python3 build_all.py        只重建網站：python3 build_all.py web
換了 Logo（web/logo.svg）要重產圖示時加上 icons：python3 build_all.py icons（需要 playwright）"""
import subprocess, sys
steps = [['scripts/export_data.py'], ['scripts/build_web.py']]
if 'web' not in sys.argv: steps.insert(0, ['scripts/build_pdf.py'])
if 'icons' in sys.argv: steps[0:0] = [['scripts/make_icons.py'], ['scripts/make_og.py']]
for s in steps:
    print('==>', s[0]); subprocess.run([sys.executable] + s, check=True)
