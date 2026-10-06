"""Build the Skill360 logo system.

usage: python build_logo.py <scratch_dir> <unbounded.ttf> <manrope.ttf> <out_dir>

Writes:
  <out_dir>/logo_data.json      geometry for the website / charte builders
  <out_dir>/sprite.svg          <symbol> sprite used by the charte HTML
  <out_dir>/svg/*.svg           the official logo files
"""
import sys, json, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[1])
from logo_geom import *

UNB, MAN, OUT = sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)

# ----------------------------------------------------------------- brand constants
C = dict(
    nuit="#070B1F", indigo="#121A44", orbite="#2F6BFF", halo="#6FE0FF", fumee="#EEF2FA",
    cyan="#1EC8F7", blanc="#FFFFFF", noir="#000000",
)
GRAD_POS = (C["cyan"], C["orbite"])   # on light backgrounds
GRAD_NEG = (C["halo"], C["orbite"])   # on dark backgrounds

U = 8                     # 1 U = 8 font units  ->  Orbite diameter = 100 U
D = 100 * U               # Orbite outer diameter
T = 24 * U                # ring thickness
GAP = 6 * U               # "échappement": cuts of the Orbite AND dot-to-stem gap
TIP = 11 * U              # chevron depth
DOT = 28 * U              # diameter of the point (i dot / centre point)
CUTS = (15, 135, 255)     # clockwise from 12 o'clock, every 120°
TRACK = -24               # logotype tracking (font units)
OLSB = 60                 # space before the Orbite
CY = -375                 # Orbite centre (half cap height)

unb = Font(UNB, 800)
man = Font(MAN, 600)
gi = unb.tt.getBestCmap()[ord("i")]


def compose_word(text, x0=0.0, base=0.0):
    """Return list of (name, d, bounds) for text set in Unbounded 800 at (x0, base)."""
    out = []
    x = x0
    for g, adv, xo, yo in unb.shape(text):
        b = unb.glyph_bounds(g)
        if g == gi:
            cont = unb.contours(g)
            dot = max(cont, key=lambda c: Font.contour_bounds(c)[1])
            stem = [c for c in cont if c is not dot]
            sx0, sy0, sx1, sy1 = Font.contour_bounds(stem[0])
            d = "".join(unb.contour_path(c, x + xo, base) for c in stem)
            out.append(("i", d, (x + xo + sx0, base - sy1, x + xo + sx1, base - sy0)))
            dcx = x + xo + (sx0 + sx1) / 2
            dcy = base - (sy1 + GAP + DOT / 2)
            out.append(("dot", circle_path(dcx, dcy, DOT / 2),
                        (dcx - DOT / 2, dcy - DOT / 2, dcx + DOT / 2, dcy + DOT / 2), (dcx, dcy)))
        else:
            name = unb.tt.getBestCmap()
            out.append((g, unb.glyph_path(g, x + xo, base),
                        (x + xo + b[0], base - b[3], x + xo + b[2], base - b[1])))
        x += adv + TRACK
    return out, x


def orbit_at(x_after, base=0.0):
    R = D / 2
    cx = x_after + OLSB + R
    cy = base + CY
    segs, cutdata = orbit_segments(cx, cy, R, R - T, CUTS, GAP, TIP)
    return dict(cx=cx, cy=cy, R=R, r=R - T, segs=segs, cutdata=cutdata,
                bounds=(cx - R, cy - R, cx + R, cy + R))


def union(bs):
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def tagline(text, width, x0, cap_top, size):
    gl = man.shape(text)
    s = size / man.upm
    first = man.glyph_bounds(gl[0][0])
    last = man.glyph_bounds(gl[-1][0])
    natural = sum(a for _, a, _, _ in gl) * s
    ink = natural - first[0] * s - (gl[-1][1] - last[2]) * s
    track = (width - ink) / (len(gl) - 1)
    base = cap_top + man.cap * s
    x = x0 - first[0] * s
    ds, bs = [], []
    for g, adv, xo, yo in gl:
        b = man.glyph_bounds(g)
        if b:
            ds.append(man.glyph_path(g, x, base, s))
            bs.append((x + b[0] * s, base - b[3] * s, x + b[2] * s, base - b[1] * s))
        x += adv * s + track
    TAG_GLYPHS[:] = ds
    return "".join(ds), union(bs), track / size


TAG_GLYPHS = []


# ----------------------------------------------------------------- horizontal logotype
word, x_end = compose_word("Skill36")
orb = orbit_at(x_end)
skill_names = {"S", "k", "i", "l"}
letters = []   # for the website animation
for item in word:
    name = item[0]
    letters.append(dict(name=name, d=item[1], bounds=item[2], **({"center": item[3]} if name == "dot" else {})))
logo_bounds = union([it["bounds"] for it in letters] + [orb["bounds"]])
LX0, LY0, LX1, LY1 = logo_bounds
LW = LX1 - LX0
x360 = [l for l in letters if l["name"] == "three"][0]["bounds"][0]

TAG_TEXT = "FORMATION & DÉVELOPPEMENT DES COMPÉTENCES"
TAG_SIZE = 132
tag_d, tag_b, tag_track = tagline(TAG_TEXT, LW, LX0, 168, TAG_SIZE)
tag_glyphs = list(TAG_GLYPHS)
print("logotype bounds", [round(v, 1) for v in logo_bounds], "W", round(LW, 1), "tag", [round(v, 1) for v in tag_b], "track em", round(tag_track, 3))

# ----------------------------------------------------------------- stacked (carré) version
LINE2 = 1040                   # baseline of second line
w1, x1e = compose_word("Skill")
w2, x2e = compose_word("36", 0, LINE2)
orb2 = orbit_at(x2e, LINE2)
b1 = union([it[2] for it in w1])
b2 = union([it[2] for it in w2] + [orb2["bounds"]])
# centre both lines on the wider one
wmax = max(b1[2] - b1[0], b2[2] - b2[0])
dx1 = (wmax - (b1[2] - b1[0])) / 2 - b1[0]
dx2 = (wmax - (b2[2] - b2[0])) / 2 - b2[0]
w1, _ = compose_word("Skill", dx1)
w2, x2e = compose_word("36", dx2, LINE2)
orb2 = orbit_at(x2e, LINE2)
sq_bounds = union([it[2] for it in w1] + [it[2] for it in w2] + [orb2["bounds"]])
print("stacked bounds", [round(v, 1) for v in sq_bounds], "line widths", round(b1[2] - b1[0]), round(b2[2] - b2[0]))

# ----------------------------------------------------------------- symbol (Orbite + point)
SYM_R = D / 2
sym = orbit_at(-OLSB - SYM_R, 0)        # centre at x=0
sym_cx, sym_cy = sym["cx"], sym["cy"]
sym_dot = circle_path(sym_cx, sym_cy, DOT / 2)
sym_bounds = sym["bounds"]


# ----------------------------------------------------------------- SVG writers
def vb(b, pad=0):
    return f"{fmt(b[0] - pad)} {fmt(b[1] - pad)} {fmt(b[2] - b[0] + 2 * pad)} {fmt(b[3] - b[1] + 2 * pad)}"



def grad_def(gid, colors, b):
    """Per-element gradient: from the top (slightly right) to the bottom (slightly left) of bounds b."""
    w = b[2] - b[0]
    x1, y1, x2, y2 = b[0] + 0.62 * w, b[1], b[0] + 0.38 * w, b[3]
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{fmt(x1)}" y1="{fmt(y1)}" '
            f'x2="{fmt(x2)}" y2="{fmt(y2)}"><stop offset="0" stop-color="{colors[0]}"/>'
            f'<stop offset="1" stop-color="{colors[1]}"/></linearGradient>')


def bounds_of(items, name):
    return [it for it in items if it[0] == name][0][2]


# element bounds per lockup
B_H = dict(three=[l for l in letters if l["name"] == "three"][0]["bounds"],
           six=[l for l in letters if l["name"] == "six"][0]["bounds"],
           orb=orb["bounds"],
           dot=[l for l in letters if l["name"] == "dot"][0]["bounds"])
B_SQ = dict(three=bounds_of(w2, "three"), six=bounds_of(w2, "six"), orb=orb2["bounds"], dot=bounds_of(w1, "dot"))
SYM_DOT_B = (sym_cx - DOT / 2, sym_cy - DOT / 2, sym_cx + DOT / 2, sym_cy + DOT / 2)
B_SYM = dict(orb=sym["bounds"], dot=SYM_DOT_B)


def defs_for(prefix, colors, B):
    return "".join(grad_def(f"{prefix}{k}", colors, b) for k, b in B.items())


def paint(spec, prefix, key):
    """spec is either a (c1, c2) gradient tuple or a flat colour string."""
    return f"url(#{prefix}{key})" if isinstance(spec, tuple) else spec


def logotype_body(skill_fill, n360, prefix="g", with_tag=False, tag_fill=None):
    p = []
    for l in letters:
        n = l["name"]
        if n in ("three", "six", "dot"):
            fill = paint(n360, prefix, n)
        else:
            fill = skill_fill
        p.append(f'<path d="{l["d"]}" fill="{fill}"/>')
    p += [f'<path d="{s}" fill="{paint(n360, prefix, "orb")}"/>' for s in orb["segs"]]
    if with_tag:
        p.append(f'<path d="{tag_d}" fill="{tag_fill or skill_fill}"/>')
    return "".join(p)


def stacked_body(skill_fill, n360, prefix="g"):
    p = []
    for it in w1:
        fill = paint(n360, prefix, "dot") if it[0] == "dot" else skill_fill
        p.append(f'<path d="{it[1]}" fill="{fill}"/>')
    for it in w2:
        p.append(f'<path d="{it[1]}" fill="{paint(n360, prefix, it[0])}"/>')
    p += [f'<path d="{s}" fill="{paint(n360, prefix, "orb")}"/>' for s in orb2["segs"]]
    return "".join(p)


def symbol_body(spec, prefix="g"):
    p = [f'<path d="{s}" fill="{paint(spec, prefix, "orb")}"/>' for s in sym["segs"]]
    p.append(f'<path d="{sym_dot}" fill="{paint(spec, prefix, "dot")}"/>')
    return "".join(p)


def write_svg(name, viewbox, defs, body, title, bg=None):
    w, h = [float(v) for v in viewbox.split()[2:]]
    rect = f'<rect x="{viewbox.split()[0]}" y="{viewbox.split()[1]}" width="{fmt(w)}" height="{fmt(h)}" fill="{bg}"/>' if bg else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" width="{fmt(w / 10)}" height="{fmt(h / 10)}" '
           f'role="img" aria-labelledby="t"><title id="t">{title}</title>'
           f'{"<defs>" + defs + "</defs>" if defs else ""}{rect}{body}</svg>\n')
    with open(os.path.join(OUT, "svg", name), "w", encoding="utf-8") as fh:
        fh.write(svg)


h_tag_bounds = union([logo_bounds, tag_b])
VB_H = vb(logo_bounds)
VB_HT = vb(h_tag_bounds)
VB_SQ = vb(sq_bounds)
VB_SYM = vb(sym_bounds)

TITLE = "Skill360 — Formation &amp; développement des compétences"
# principal (with tagline)
write_svg("skill360-logo-principal.svg", VB_HT, defs_for("g", GRAD_POS, B_H),
          logotype_body(C["nuit"], GRAD_POS, "g", True), TITLE)
write_svg("skill360-logo-principal-negatif.svg", VB_HT, defs_for("g", GRAD_NEG, B_H),
          logotype_body(C["fumee"], GRAD_NEG, "g", True), TITLE)
# logotype
write_svg("skill360-logotype.svg", VB_H, defs_for("g", GRAD_POS, B_H), logotype_body(C["nuit"], GRAD_POS), "Skill360")
write_svg("skill360-logotype-negatif.svg", VB_H, defs_for("g", GRAD_NEG, B_H), logotype_body(C["fumee"], GRAD_NEG), "Skill360")
# flat & mono
write_svg("skill360-logotype-aplat.svg", VB_H, "", logotype_body(C["nuit"], C["orbite"]), "Skill360")
write_svg("skill360-logotype-aplat-negatif.svg", VB_H, "", logotype_body(C["fumee"], C["halo"]), "Skill360")
write_svg("skill360-logotype-mono-nuit.svg", VB_H, "", logotype_body(C["nuit"], C["nuit"]), "Skill360")
write_svg("skill360-logotype-mono-noir.svg", VB_H, "", logotype_body(C["noir"], C["noir"]), "Skill360")
write_svg("skill360-logotype-mono-blanc.svg", VB_H, "", logotype_body(C["blanc"], C["blanc"]), "Skill360")
write_svg("skill360-logo-principal-mono-nuit.svg", VB_HT, "", logotype_body(C["nuit"], C["nuit"], "g", True), TITLE)
write_svg("skill360-logo-principal-mono-blanc.svg", VB_HT, "", logotype_body(C["blanc"], C["blanc"], "g", True), TITLE)
# stacked
write_svg("skill360-logo-carre.svg", VB_SQ, defs_for("g", GRAD_POS, B_SQ), stacked_body(C["nuit"], GRAD_POS), "Skill360")
write_svg("skill360-logo-carre-negatif.svg", VB_SQ, defs_for("g", GRAD_NEG, B_SQ), stacked_body(C["fumee"], GRAD_NEG), "Skill360")
# symbol
write_svg("skill360-orbite.svg", VB_SYM, defs_for("g", GRAD_POS, B_SYM), symbol_body(GRAD_POS), "Skill360 — l'Orbite")
write_svg("skill360-orbite-negatif.svg", VB_SYM, defs_for("g", GRAD_NEG, B_SYM), symbol_body(GRAD_NEG), "Skill360 — l'Orbite")
write_svg("skill360-orbite-mono-nuit.svg", VB_SYM, "", symbol_body(C["nuit"]), "Skill360 — l'Orbite")
write_svg("skill360-orbite-mono-blanc.svg", VB_SYM, "", symbol_body(C["blanc"]), "Skill360 — l'Orbite")

# app icon / favicon: Orbite on a Nuit square (padding 22 %)
pad = D * 0.22
ib = (sym_bounds[0] - pad, sym_bounds[1] - pad, sym_bounds[2] + pad, sym_bounds[3] + pad)
VB_ICON = vb(ib)
write_svg("skill360-icone-app.svg", VB_ICON, defs_for("g", GRAD_NEG, B_SYM), symbol_body(GRAD_NEG), "Skill360", bg=C["nuit"])
# favicon: flat Halo cyan (gradients vanish under 32 px)
write_svg("skill360-favicon.svg", VB_ICON, "", symbol_body(C["halo"]), "Skill360", bg=C["nuit"])


# ----------------------------------------------------------------- sprite for HTML documents
def css_fill(var, fallback):
    return f'style="fill:var({var},{fallback})"'


def sprite_logotype(sid, with_tag):
    skill_fb = C["fumee"] if sid.endswith("-neg") else C["nuit"]
    p = []
    for l in letters:
        n = l["name"]
        if n in ("three", "six"):
            p.append(f'<path d="{l["d"]}" {css_fill("--l360", f"url(#{sid}-{n})")}/>')
        elif n == "dot":
            p.append(f'<path d="{l["d"]}" {css_fill("--ldot", f"var(--l360,url(#{sid}-dot))")}/>')
        else:
            p.append(f'<path d="{l["d"]}" {css_fill("--lskill", skill_fb)}/>')
    p += [f'<path d="{s}" {css_fill("--lorb", f"var(--l360,url(#{sid}-orb))")}/>' for s in orb["segs"]]
    if with_tag:
        p.append(f'<path d="{tag_d}" {css_fill("--ltag", f"var(--lskill,{skill_fb})")}/>')
    return f'<symbol id="{sid}" viewBox="{VB_HT if with_tag else VB_H}">{"".join(p)}</symbol>'


def sprite_stacked(sid):
    skill_fb = C["fumee"] if sid.endswith("-neg") else C["nuit"]
    p = []
    for it in w1:
        if it[0] == "dot":
            p.append(f'<path d="{it[1]}" {css_fill("--ldot", f"var(--l360,url(#{sid}-dot))")}/>')
        else:
            p.append(f'<path d="{it[1]}" {css_fill("--lskill", skill_fb)}/>')
    for it in w2:
        p.append(f'<path d="{it[1]}" {css_fill("--l360", f"url(#{sid}-{it[0]})")}/>')
    p += [f'<path d="{s}" {css_fill("--lorb", f"var(--l360,url(#{sid}-orb))")}/>' for s in orb2["segs"]]
    return f'<symbol id="{sid}" viewBox="{VB_SQ}">{"".join(p)}</symbol>'


def sprite_symbol(sid):
    p = [f'<path d="{s}" {css_fill("--lorb", f"var(--l360,url(#{sid}-orb))")}/>' for s in sym["segs"]]
    p.append(f'<path d="{sym_dot}" {css_fill("--ldot", f"var(--l360,url(#{sid}-dot))")}/>')
    return f'<symbol id="{sid}" viewBox="{VB_SYM}">{"".join(p)}</symbol>'


defs = "".join([
    defs_for("logo-h-", GRAD_POS, B_H), defs_for("logo-h-neg-", GRAD_NEG, B_H),
    defs_for("logotype-", GRAD_POS, B_H), defs_for("logotype-neg-", GRAD_NEG, B_H),
    defs_for("logo-sq-", GRAD_POS, B_SQ), defs_for("logo-sq-neg-", GRAD_NEG, B_SQ),
    defs_for("orbite-", GRAD_POS, B_SYM), defs_for("orbite-neg-", GRAD_NEG, B_SYM),
])
sprite = (f'<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true">'
          f'<defs>{defs}</defs>'
          + sprite_logotype("logo-h", True) + sprite_logotype("logo-h-neg", True)
          + sprite_logotype("logotype", False) + sprite_logotype("logotype-neg", False)
          + sprite_stacked("logo-sq") + sprite_stacked("logo-sq-neg")
          + sprite_symbol("orbite") + sprite_symbol("orbite-neg")
          + "</svg>")
with open(os.path.join(OUT, "sprite.svg"), "w", encoding="utf-8") as fh:
    fh.write(sprite)


def grad_coords(b):
    w = b[2] - b[0]
    return (b[0] + 0.62 * w, b[1], b[0] + 0.38 * w, b[3])


def grad_coords_h():
    return {k: grad_coords(b) for k, b in B_H.items()}


def grad_coords_sym():
    return {k: grad_coords(b) for k, b in B_SYM.items()}

# ----------------------------------------------------------------- morph shapes for the website
R = D / 2
cx, cy = orb["cx"], orb["cy"]
thin, _ = orbit_segments(cx, cy, R, R - 14, CUTS, 0, 0)            # a thin, closed orbit line
wedge, _ = orbit_segments(cx, cy, R * 0.32, 2, CUTS, 0, 0)          # a small disc cut in 3 (the point)
fat, _ = orbit_segments(cx, cy, R, R - T * 1.5, CUTS, GAP * 1.6, TIP * 1.6)  # over-shoot shape

data = dict(
    unit=U, D=D, T=T, gap=GAP, tip=TIP, dot=DOT, cuts=CUTS, track=TRACK,
    colors=C, grad_pos=GRAD_POS, grad_neg=GRAD_NEG,
    logo_bounds=logo_bounds, logo_tag_bounds=h_tag_bounds, square_bounds=sq_bounds, symbol_bounds=sym_bounds,
    viewbox_h=VB_H, viewbox_ht=VB_HT, viewbox_sq=VB_SQ, viewbox_sym=VB_SYM, viewbox_icon=VB_ICON,
    grad_h=grad_coords_h(), grad_sym=grad_coords_sym(),
    letters=letters, orbit=dict(cx=cx, cy=cy, R=R, r=R - T, segs=orb["segs"], thin=thin, wedge=wedge, fat=fat,
                                cutdata=orb["cutdata"]),
    tagline=dict(d=tag_d, glyphs=tag_glyphs, bounds=tag_b, size=TAG_SIZE, track_em=tag_track, text=TAG_TEXT),
    symbol=dict(cx=sym_cx, cy=sym_cy, segs=sym["segs"], dot=sym_dot),
    stacked=dict(w1=[(a[0], a[1]) for a in w1], w2=[(a[0], a[1]) for a in w2], segs=orb2["segs"]),
)
with open(os.path.join(OUT, "logo_data.json"), "w", encoding="utf-8") as fh:
    json.dump(data, fh)
print("ok — files:", sorted(os.listdir(os.path.join(OUT, "svg"))))
