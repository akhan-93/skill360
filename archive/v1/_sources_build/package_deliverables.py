"""Assemble the SKILL360_Identite delivery folder.
usage: python package_deliverables.py <scratch_dir> <deliverables_root>
"""
import os, sys, json, shutil, struct
sys.stdout.reconfigure(encoding="utf-8")
SCRATCH, ROOT = sys.argv[1], sys.argv[2]
from PIL import Image


def d(*p):
    path = os.path.join(ROOT, *p)
    os.makedirs(path, exist_ok=True)
    return path


# ------------------------------------------------------------------ 01 charte
charte_dir = d("01_Charte_graphique")
shutil.copy(os.path.join(SCRATCH, "charte", "charte.pdf"), os.path.join(charte_dir, "Skill360_Charte_graphique_V1.0.pdf"))
src = os.path.join(charte_dir, "source")
if os.path.isdir(src):
    shutil.rmtree(src)
os.makedirs(src)
for f in ("charte.html", "charte.css"):
    shutil.copy(os.path.join(SCRATCH, "charte", f), os.path.join(src, f))
for sub in ("fonts", "logos"):
    shutil.copytree(os.path.join(SCRATCH, "charte", sub), os.path.join(src, sub))
os.makedirs(os.path.join(src, "img"))
for f in os.listdir(os.path.join(SCRATCH, "charte", "img")):
    if f.endswith(".jpg"):
        shutil.copy(os.path.join(SCRATCH, "charte", "img", f), os.path.join(src, "img", f))

# ------------------------------------------------------------------ 02 logo (SVG + favicon extras; PNG already rendered)
svg_dir = d("02_Logo", "SVG")
for f in os.listdir(os.path.join(SCRATCH, "build", "svg")):
    if f.endswith(".svg"):
        target = svg_dir if f not in ("skill360-favicon.svg", "skill360-icone-app.svg") else d("02_Logo", "Favicon")
        shutil.copy(os.path.join(SCRATCH, "build", "svg", f), os.path.join(target, f))
fav = d("02_Logo", "Favicon")
ico_src = Image.open(os.path.join(fav, "favicon-256.png")).convert("RGBA")
ico_src.save(os.path.join(fav, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# ------------------------------------------------------------------ 03 couleurs
colors = json.load(open(os.path.join(SCRATCH, "build", "colors.json"), encoding="utf-8"))["palette"]
col_dir = d("03_Couleurs")
slug = {"Nuit spatiale": "nuit", "Indigo profond": "indigo", "Bleu orbite": "orbite", "Halo cyan": "halo",
        "Fumée blanche": "fumee", "Cyan vif": "cyan", "Ardoise": "ardoise", "Brume": "brume"}
css = ["/* Skill360 — couleurs de marque (charte graphique V1.0) */", ":root {"]
for c in colors:
    css.append(f"  --s360-{slug[c['name']]}: {c['hex']}; /* {c['name']} — {c['use']} */")
css += ["  --s360-orbite-ui: #2D69FC; /* Bleu orbite, valeur interface : boutons à libellé blanc (4,62:1) */",
        "  --s360-degrade-orbite: linear-gradient(165deg, #1EC8F7, #2F6BFF); /* « 360 » sur fond clair */",
        "  --s360-degrade-halo: linear-gradient(165deg, #6FE0FF, #2F6BFF); /* « 360 » sur fond sombre */",
        "}", ""]
open(os.path.join(col_dir, "skill360-couleurs.css"), "w", encoding="utf-8").write("\n".join(css))
out = {"couleurs": [{"nom": c["name"], "hex": c["hex"], "rvb": c["rgb"], "cmjn_indicatif": c["cmyk"], "usage": c["use"]} for c in colors],
       "valeur_interface": {"nom": "Bleu orbite — interface", "hex": "#2D69FC", "usage": "Boutons à libellé blanc"},
       "degrades": {"orbite": ["#1EC8F7", "#2F6BFF"], "halo": ["#6FE0FF", "#2F6BFF"]},
       "note": "CMJN : conversion indicative sans profil ICC, à valider sur épreuve. Pantone : à arrêter avec l'imprimeur."}
json.dump(out, open(os.path.join(col_dir, "skill360-couleurs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def ase(entries):
    """Adobe Swatch Exchange (RGB, global colours)."""
    blocks = b""
    for name, hx in entries:
        r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
        n = (name + "\0").encode("utf-16-be")
        body = struct.pack(">H", len(name) + 1) + n + b"RGB " + struct.pack(">fff", r, g, b) + struct.pack(">H", 0)
        blocks += struct.pack(">HI", 0x0001, len(body)) + body
    return b"ASEF" + struct.pack(">HHI", 1, 0, len(entries)) + blocks


entries = [(f"Skill360 {c['name']}", c["hex"]) for c in colors] + [("Skill360 Bleu orbite interface", "#2D69FC")]
open(os.path.join(col_dir, "skill360-palette.ase"), "wb").write(ase(entries))

# ------------------------------------------------------------------ 04 typographies
fonts = os.path.join(SCRATCH, "dl_fonts")
for fam, ttf, lic in (("Unbounded", "Unbounded-VF.ttf", "Unbounded-OFL.txt"), ("Manrope", "Manrope-VF.ttf", "Manrope-OFL.txt")):
    fd = d("04_Typographies", fam)
    shutil.copy(os.path.join(fonts, ttf), os.path.join(fd, f"{fam}-VariableFont_wght.ttf"))
    shutil.copy(os.path.join(fonts, lic), os.path.join(fd, "OFL.txt"))
web = d("04_Typographies", "Web")
for f in os.listdir(os.path.join(SCRATCH, "build", "fonts")):
    shutil.copy(os.path.join(SCRATCH, "build", "fonts", f), os.path.join(web, f))

# summary
for base, dirs, files in os.walk(ROOT):
    depth = base[len(ROOT):].count(os.sep)
    if depth > 2 or "assets" in base or "source" in base:
        continue
    print("  " * depth + os.path.basename(base) + "/", f"({len(files)} fichiers)" if files else "")
