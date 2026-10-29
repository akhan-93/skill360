"""Assemble charte.html (Skill360 brand guidelines). usage: python build_charte.py <scratch_dir>"""
import os, sys, shutil
sys.stdout.reconfigure(encoding="utf-8")
SCRATCH = sys.argv[1]
sys.path.insert(0, SCRATCH)

from PIL import Image
import charte_lib as L
import charte_p1  # noqa: F401  (registers pages)
import charte_p2  # noqa: F401

OUT = os.path.join(SCRATCH, "charte")
os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
os.makedirs(os.path.join(OUT, "logos"), exist_ok=True)
for f in os.listdir(os.path.join(SCRATCH, "build", "fonts")):
    shutil.copy(os.path.join(SCRATCH, "build", "fonts", f), os.path.join(OUT, "fonts", f))
for f in os.listdir(os.path.join(SCRATCH, "build", "svg")):
    if f.endswith(".svg"):
        shutil.copy(os.path.join(SCRATCH, "build", "svg", f), os.path.join(OUT, "logos", f))

# screenshots -> jpg (lighter PDF)
img = os.path.join(OUT, "img")
for f in os.listdir(img):
    if f.endswith(".png"):
        im = Image.open(os.path.join(img, f)).convert("RGB")
        if im.width > 2200:
            im = im.resize((2200, round(im.height * 2200 / im.width)), Image.LANCZOS)
        im.save(os.path.join(img, f[:-4] + ".jpg"), quality=86, optimize=True, progressive=True)

sprite = open(os.path.join(SCRATCH, "build", "sprite.svg"), encoding="utf-8").read()
icons = open(os.path.join(SCRATCH, "site_src", "icons.svg"), encoding="utf-8").read()
html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>Skill360 — Charte graphique V1.0</title>
<link rel="stylesheet" href="charte.css">
</head><body>
{sprite}
{icons}
{L.render_pages()}
</body></html>"""
open(os.path.join(OUT, "charte.html"), "w", encoding="utf-8").write(html)
print("pages:", len(L.PAGES), "html bytes:", len(html))
