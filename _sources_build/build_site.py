"""Assemble the Skill360 website.

usage: python build_site.py <scratch_dir> <logo_data.json> <site_src_dir> <logo_build_dir> <dest_dir>

- injects the animatable hero logo (<!-- @HERO_LOGO -->) and the big Orbite
  (<!-- @DIM_ORBIT -->) into every *.src.html template of site_src
- copies css / js / fonts / images / GSAP vendor files to dest
"""
import sys, os, json, math, shutil
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[1])
from logo_geom import fmt, polar, orbit_segments, circle_path

SCRATCH, DATA, SRC, LOGOBUILD, DEST = sys.argv[1:6]
d = json.load(open(DATA, encoding="utf-8"))
C = d["colors"]
HALO, ORBITE, FUMEE, CYAN = C["halo"], C["orbite"], C["fumee"], C["cyan"]


def gcoords(b):
    w = b[2] - b[0]
    return b[0] + 0.62 * w, b[1], b[0] + 0.38 * w, b[3]


def lin(gid, b, c1, c2):
    x1, y1, x2, y2 = gcoords(b)
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{fmt(x1)}" y1="{fmt(y1)}" '
            f'x2="{fmt(x2)}" y2="{fmt(y2)}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


# ------------------------------------------------------------------ hero logo (animatable)
def hero_logo(uid="lg"):
    L = d["letters"]
    O = d["orbit"]
    T = d["tagline"]
    lb = d["logo_bounds"]
    tb = d["logo_tag_bounds"]
    padx, padt, padb = 300, 360, 140
    vb = f"{fmt(tb[0] - padx)} {fmt(tb[1] - padt)} {fmt(tb[2] - tb[0] + 2 * padx)} {fmt(tb[3] - tb[1] + padt + padb)}"
    lcx = (lb[0] + lb[2]) / 2
    ocx, ocy, R = O["cx"], O["cy"], O["R"]
    dot = [l for l in L if l["name"] == "dot"][0]
    dcx, dcy = dot["center"]
    by = {l["name"]: l for l in L}
    ob = (ocx - R, ocy - R, ocx + R, ocy + R)
    defs = (lin(f"{uid}-g3", by["three"]["bounds"], HALO, ORBITE)
            + lin(f"{uid}-g6", by["six"]["bounds"], HALO, ORBITE)
            + lin(f"{uid}-go", ob, HALO, ORBITE)
            + lin(f"{uid}-gd", dot["bounds"], HALO, ORBITE)
            + f'<radialGradient id="{uid}-halo"><stop offset="0" stop-color="{HALO}" stop-opacity=".42"/>'
              f'<stop offset=".38" stop-color="{ORBITE}" stop-opacity=".16"/>'
              f'<stop offset="1" stop-color="{ORBITE}" stop-opacity="0"/></radialGradient>')
    letters = []
    for l in L:
        n = l["name"]
        if n == "dot":
            continue
        if n in ("three", "six"):
            fill = f"url(#{uid}-g{'3' if n == 'three' else '6'})"
            cls = "lg-ltr lg-360"
        else:
            fill = FUMEE
            cls = "lg-ltr"
        letters.append(f'<path class="{cls}" d="{l["d"]}" fill="{fill}" stroke="{HALO}" stroke-width="9" stroke-opacity="0" '
                       f'stroke-linejoin="round"/>')
    segs = []
    for s_thin, s_fat, s_fin in zip(O["thin"], O["fat"], O["segs"]):
        segs.append(f'<path class="lg-seg" d="{s_fin}" data-thin="{s_thin}" data-fat="{s_fat}" data-final="{s_fin}" '
                    f'fill="url(#{uid}-go)"/>')
    tag = "".join(f'<path class="lg-tg" d="{g}"/>' for g in T["glyphs"])
    return (
        f'<svg class="lg" viewBox="{vb}" role="img" aria-labelledby="{uid}-title" overflow="visible" '
        f'data-lcx="{fmt(lcx)}" data-ocx="{fmt(ocx)}" data-ocy="{fmt(ocy)}" data-dcx="{fmt(dcx)}" data-dcy="{fmt(dcy)}">'
        f'<title id="{uid}-title">Skill360 — Formation &amp; développement des compétences</title>'
        f'<defs>{defs}</defs>'
        f'<g class="lg-letters">{"".join(letters)}</g>'
        f'<g class="lg-orbit-move">'
        f'<circle class="lg-halo" cx="{fmt(ocx)}" cy="{fmt(ocy)}" r="{fmt(R * 1.9)}" fill="url(#{uid}-halo)" opacity="0"/>'
        f'<g class="lg-orbit-spin">'
        f'<circle class="lg-trace" cx="{fmt(ocx)}" cy="{fmt(ocy)}" r="{fmt(R - 7)}" fill="none" stroke="{HALO}" '
        f'stroke-width="14" opacity="0" transform="rotate(-90 {fmt(ocx)} {fmt(ocy)})"/>'
        f'{"".join(segs)}</g></g>'
        f'<path class="lg-dot" d="{dot["d"]}" fill="url(#{uid}-gd)"/>'
        f'<g class="lg-tag" fill="{FUMEE}">{tag}</g>'
        f'</svg>'
    )


# ------------------------------------------------------------------ big Orbite for the "dimensions" section
def dim_orbit():
    S = d["symbol"]
    cx, cy = S["cx"], S["cy"]
    R = d["D"] / 2
    r = R - d["T"]
    segs, _ = orbit_segments(cx, cy, R, r, d["cuts"], d["gap"], d["tip"])
    ob = (cx - R, cy - R, cx + R, cy + R)
    db = (cx - d["dot"] / 2, cy - d["dot"] / 2, cx + d["dot"] / 2, cy + d["dot"] / 2)
    cuts = d["cuts"]
    # segment k spans cuts[k] -> cuts[k+1]
    mids = [((cuts[k] + ((cuts[(k + 1) % 3] - cuts[k]) % 360) / 2) % 360) for k in range(3)]
    labels = {2: "Savoir", 0: "Savoir-faire", 1: "Savoir-être"}       # reading order: top-left, right, bottom
    order = [2, 0, 1]
    paths, texts = [], []
    LR = R + 120
    for k in range(3):
        m = mids[k]
        a0, a1 = m - 48, m + 48
        bottom = 90 < m < 270
        if bottom:  # run counter-clockwise so the text is not upside down
            p0, p1 = polar(cx, cy, LR + 44, a1), polar(cx, cy, LR + 44, a0)
            arc = f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(LR + 44)} {fmt(LR + 44)} 0 0 0 {fmt(p1[0])} {fmt(p1[1])}"
        else:
            p0, p1 = polar(cx, cy, LR, a0), polar(cx, cy, LR, a1)
            arc = f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(LR)} {fmt(LR)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
        paths.append(f'<path id="dim-arc-{k}" d="{arc}" fill="none"/>')
        texts.append(f'<text class="dim-label" data-seg="{k}"><textPath href="#dim-arc-{k}" startOffset="50%" '
                     f'text-anchor="middle">{labels[k]}</textPath></text>')
    seg_el = "".join(
        f'<path class="dim-seg" data-seg="{k}" data-mid="{fmt(mids[k])}" d="{segs[k]}" fill="url(#dim-go)"/>' for k in range(3))
    pad = 330
    vb = f"{fmt(cx - R - pad)} {fmt(cy - R - pad)} {fmt(2 * (R + pad))} {fmt(2 * (R + pad))}"
    return (
        f'<svg class="dim-orbit" viewBox="{vb}" aria-hidden="true">'
        f'<defs>{lin("dim-go", ob, HALO, ORBITE)}{lin("dim-gd", db, HALO, ORBITE)}{"".join(paths)}</defs>'
        f'<circle class="dim-ring" cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R + 60)}" fill="none"/>'
        f'<circle class="dim-progress" cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R + 60)}" fill="none" '
        f'transform="rotate(-90 {fmt(cx)} {fmt(cy)})"/>'
        f'<g class="dim-segs">{seg_el}</g>'
        f'<path class="dim-dot" d="{circle_path(cx, cy, d["dot"] / 2)}" fill="url(#dim-gd)"/>'
        f'{"".join(texts)}'
        f'</svg>'
    )


# ------------------------------------------------------------------ small inline Orbite (separators, decor)
def mini_orbit(cls="mini-orbit"):
    S = d["symbol"]
    cx, cy = S["cx"], S["cy"]
    R = d["D"] / 2
    vb = f"{fmt(cx - R)} {fmt(cy - R)} {fmt(2 * R)} {fmt(2 * R)}"
    segs = "".join(f'<path d="{s}"/>' for s in S["segs"])
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true" focusable="false">{segs}<path d="{S["dot"]}"/></svg>'


REPL = {
    "<!-- @HERO_LOGO -->": hero_logo("lg"),
    "<!-- @DIM_ORBIT -->": dim_orbit(),
    "<!-- @MINI_ORBIT -->": mini_orbit(),
    "<!-- @ICONS -->": open(os.path.join(SRC, "icons.svg"), encoding="utf-8").read(),
}

# ------------------------------------------------------------------ copy + render templates
if os.path.isdir(DEST):
    for name in ("index.html", "animation-logo.html"):
        p = os.path.join(DEST, name)
        if os.path.exists(p):
            os.remove(p)
    if os.path.isdir(os.path.join(DEST, "assets")):
        shutil.rmtree(os.path.join(DEST, "assets"))
os.makedirs(DEST, exist_ok=True)
shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DEST, "assets"))
os.makedirs(os.path.join(DEST, "assets", "fonts"), exist_ok=True)
for f in os.listdir(os.path.join(LOGOBUILD, "fonts")):
    shutil.copy(os.path.join(LOGOBUILD, "fonts", f), os.path.join(DEST, "assets", "fonts", f))
os.makedirs(os.path.join(DEST, "assets", "img"), exist_ok=True)
for f in ("skill360-logotype-negatif.svg", "skill360-logo-principal-negatif.svg", "skill360-orbite-negatif.svg",
          "skill360-favicon.svg"):
    shutil.copy(os.path.join(LOGOBUILD, "svg", f), os.path.join(DEST, "assets", "img", f))
vendor = os.path.join(DEST, "assets", "js", "vendor")
os.makedirs(vendor, exist_ok=True)
gsap_dist = os.path.join(SCRATCH, "tools", "node_modules", "gsap", "dist")
for f in ("gsap.min.js", "ScrollTrigger.min.js", "MorphSVGPlugin.min.js", "DrawSVGPlugin.min.js", "SplitText.min.js"):
    shutil.copy(os.path.join(gsap_dist, f), os.path.join(vendor, f))

for name in os.listdir(SRC):
    if name.endswith(".src.html"):
        html = open(os.path.join(SRC, name), encoding="utf-8").read()
        for k, v in REPL.items():
            html = html.replace(k, v)
        out = os.path.join(DEST, name.replace(".src.html", ".html"))
        open(out, "w", encoding="utf-8").write(html)
        print("wrote", out, len(html))
