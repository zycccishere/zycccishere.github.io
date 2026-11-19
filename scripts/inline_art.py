"""Inline assets/img/art/*.svg into index.html.

Each thumbnail lives between <!--art:NAME--> and <!--/art:NAME--> markers;
re-running replaces the block in place. On first run it replaces the old
<img src="assets/img/pubs/NAME.webp" ...> tag.
"""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html_path = root / "index.html"
html = html_path.read_text(encoding="utf-8")

for svg_file in sorted((root / "assets" / "img" / "art").glob("*.svg")):
    name = svg_file.stem
    block = f"<!--art:{name}-->{svg_file.read_text(encoding='utf-8').strip()}<!--/art:{name}-->"
    marker = re.compile(rf"<!--art:{re.escape(name)}-->.*?<!--/art:{re.escape(name)}-->", re.S)
    img = re.compile(rf'<img src="assets/img/pubs/{re.escape(name)}\.webp"[^>]*>')
    if marker.search(html):
        html = marker.sub(lambda _: block, html, count=1)
    elif img.search(html):
        html = img.sub(lambda _: block, html, count=1)
    else:
        raise SystemExit(f"no placeholder for {name}")
    print("inlined", name)

html_path.write_text(html, encoding="utf-8")
