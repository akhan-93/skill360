"""Palette values and WCAG 2.1 contrast ratios for the Skill360 charter."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

PALETTE = [
    ("Nuit spatiale", "#070B1F", "Fond principal, logotype sur fond clair"),
    ("Indigo profond", "#121A44", "Surfaces, cartes, aplats secondaires"),
    ("Bleu orbite", "#2F6BFF", "Boutons, accents, fin du dégradé"),
    ("Halo cyan", "#6FE0FF", "« 360 » sur fond sombre, lumière"),
    ("Fumée blanche", "#EEF2FA", "Textes sur fond sombre, fonds clairs"),
    ("Cyan vif", "#1EC8F7", "Début du dégradé sur fond clair"),
    ("Ardoise", "#4A5170", "Texte secondaire sur fond clair"),
    ("Brume", "#A6AFCC", "Texte secondaire sur fond sombre"),
]
WHITE = "#FFFFFF"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def cmyk(h):
    r, g, b = (v / 255 for v in rgb(h))
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return tuple(round(v * 100) for v in (c, m, y, k))


out = {"palette": [], "contrasts": []}
for name, hx, use in PALETTE:
    out["palette"].append(dict(name=name, hex=hx, rgb=rgb(hx), cmyk=cmyk(hx), use=use))
    print(f"{name:15} {hx}  RVB {rgb(hx)}  CMJN {cmyk(hx)}")

pairs = [
    ("Fumée blanche sur Nuit spatiale", "#EEF2FA", "#070B1F"),
    ("Halo cyan sur Nuit spatiale", "#6FE0FF", "#070B1F"),
    ("Brume sur Nuit spatiale", "#A6AFCC", "#070B1F"),
    ("Fumée blanche sur Indigo profond", "#EEF2FA", "#121A44"),
    ("Blanc sur Bleu orbite", "#FFFFFF", "#2F6BFF"),
    ("Bleu orbite sur Nuit spatiale", "#2F6BFF", "#070B1F"),
    ("Nuit spatiale sur Fumée blanche", "#070B1F", "#EEF2FA"),
    ("Nuit spatiale sur blanc", "#070B1F", "#FFFFFF"),
    ("Ardoise sur Fumée blanche", "#4A5170", "#EEF2FA"),
    ("Bleu orbite sur Fumée blanche", "#2F6BFF", "#EEF2FA"),
    ("Bleu orbite sur blanc", "#2F6BFF", "#FFFFFF"),
    ("Cyan vif sur blanc", "#1EC8F7", "#FFFFFF"),
    ("Halo cyan sur blanc", "#6FE0FF", "#FFFFFF"),
]
for label, fg, bg in pairs:
    r = contrast(fg, bg)
    if r >= 7:
        lvl = "AAA — tout usage"
    elif r >= 4.5:
        lvl = "AA — texte courant"
    elif r >= 3:
        lvl = "AA grands textes (≥ 18 pt) uniquement"
    else:
        lvl = "Interdit pour le texte"
    out["contrasts"].append(dict(label=label, fg=fg, bg=bg, ratio=round(r, 1), level=lvl))
    print(f"{label:38} {r:5.2f}:1  {lvl}")

json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
