"""一次重建全部：python3 build_all.py        只重建網站：python3 build_all.py web"""
import subprocess, sys
steps = [['scripts/export_data.py'], ['scripts/build_web.py']]
if 'web' not in sys.argv: steps.insert(0, ['scripts/build_pdf.py'])
for s in steps:
    print('==>', s[0]); subprocess.run([sys.executable] + s, check=True)
