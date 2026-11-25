"""Compose a trimmed two-page spread mockup (JPEG) from a 2-page layout PDF. Usage: make_spread.py in.pdf out.jpg"""
import subprocess, sys, tempfile, pathlib
from PIL import Image, ImageDraw, ImageFilter
pdf, out = sys.argv[1], sys.argv[2]
dpi = 200; b = int(0.125 * dpi)
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", "1", "-l", "2", pdf, str(tmp / "p")], check=True)
L, R = [Image.open(p) for p in sorted(tmp.glob("p-*.png"))]
w, h = L.size
L = L.crop((b, b, w, h - b)); R = R.crop((0, b, w - b, h - b))
pw, ph = L.size; pad = 120
bg = Image.new("RGB", (pw * 2 + pad * 2, ph + pad * 2), (232, 228, 220))
sh = Image.new("L", bg.size, 0); ImageDraw.Draw(sh).rectangle((pad + 10, pad + 18, pad + pw * 2 + 10, pad + ph + 18), fill=110)
bg.paste((90, 80, 70), (0, 0), sh.filter(ImageFilter.GaussianBlur(22)))
bg.paste(L, (pad, pad)); bg.paste(R, (pad + pw, pad))
g = Image.new("L", (160, ph), 0); d = ImageDraw.Draw(g)
for x in range(160): d.line((x, 0, x, ph), fill=int(55 * (1 - abs(x - 80) / 80) ** 2))
bg.paste((60, 50, 40), (pad + pw - 80, pad), g)
bg.save(out, quality=90)
