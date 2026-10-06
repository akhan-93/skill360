"""Helpers for the Skill360 brand guidelines (charte graphique) HTML generator."""
import json, math, os

SCRATCH = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(SCRATCH, "build", "logo_data.json"), encoding="utf-8"))
COLORS = json.load(open(os.path.join(SCRATCH, "build", "colors.json"), encoding="utf-8"))
C = DATA["colors"]

VB = {
    "logo-h": DATA["viewbox_ht"], "logo-h-neg": DATA["viewbox_ht"],
    "logotype": DATA["viewbox_h"], "logotype-neg": DATA["viewbox_h"],
    "logo-sq": DATA["viewbox_sq"], "logo-sq-neg": DATA["viewbox_sq"],
    "orbite": DATA["viewbox_sym"], "orbite-neg": DATA["viewbox_sym"],
}
VARS = {"skill": "--lskill", "n360": "--l360", "tag": "--ltag", "dot": "--ldot", "orb": "--lorb"}


def logo(kind="logo-h", w="60mm", style="", cls="", **v):
    """Inline logo from the sprite. Colours can be overridden: skill, n360, tag, dot, orb."""
    x, y, vw, vh = VB[kind].split()
    css = "".join(f"{VARS[k]}:{val};" for k, val in v.items())
    return (f'<svg class="L {cls}" viewBox="{VB[kind]}" style="width:{w};{css}{style}">'
            f'<use href="#{kind}" x="{x}" y="{y}" width="{vw}" height="{vh}"/></svg>')


def ratio(kind):
    _, _, vw, vh = (float(t) for t in VB[kind].split())
    return vw / vh


def icon(name, size="7mm", color=None, style=""):
    col = f"color:{color};" if color else ""
    return f'<svg class="ico" style="width:{size};height:{size};{col}{style}"><use href="#i-{name}"/></svg>'


def lbl(t):
    return f'<span class="lbl">{t}</span>'


def blk(label, html, cls=""):
    return f'<div class="blk {cls}">{lbl(label)}{html}</div>'


def txt(t, cls=""):
    return f'<p class="txt {cls}">{t}</p>'


def bul(items, cls=""):
    return f'<ul class="bul {cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def tbl(rows, head=None, widths=None, cls=""):
    cg = ""
    if widths:
        cg = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    h = ""
    if head:
        h = "<thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead>"
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="tbl {cls}">{cg}{h}<tbody>{b}</tbody></table>'


def note(label, html):
    return f'<div class="note">{lbl(label)}{html}</div>'


V = '<span class="v">[À&nbsp;VÉRIFIER]</span>'


def _lum(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast(fg, bg):
    a, b = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def ratio_txt(r):
    """WCAG ratios are thresholds: truncate (never round up) to two decimals."""
    return f"{math.floor(r * 100) / 100:.2f}".replace(".", ",") + ":1"


def wcag_level(r):
    if r >= 7:
        return "AAA — tout usage"
    if r >= 4.5:
        return "AA — texte courant"
    if r >= 3:
        return "Grands textes uniquement (≥ 18,7 px gras, 24 px)"
    return "Interdit pour le texte"


def tile(inner, bg="fumee", h="40mm", tag="", cap="", style="", extra=""):
    t = f'<span class="tag-l">{tag}</span>' if tag else ""
    c = f'<p class="cap">{cap}</p>' if cap else ""
    return (f'<div><div class="tile tile--{bg}" style="height:{h};{style}">{t}{inner}{extra}</div>{c}</div>')


def rings(cx, cy, radii, cls="", style="", sats=None, w="100%", h="100%"):
    """Decorative orbit lines (SVG in a 1000x1000 box positioned absolutely)."""
    c = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>' for r in radii)
    s = ""
    for (r, deg, rad, col) in (sats or []):
        a = math.radians(deg)
        s += f'<circle cx="{cx + r * math.sin(a):.1f}" cy="{cy - r * math.cos(a):.1f}" r="{rad}" style="fill:{col};stroke:none"/>'
    return (f'<svg class="rings {cls}" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" '
            f'style="inset:0;width:{w};height:{h};{style}">{c}{s}</svg>')


# ------------------------------------------------------------------ pages
PAGES = []          # (title, section, html)


def page(title, section, body, lead="", dark=False, cls="", toc=True, content_style=""):
    PAGES.append(dict(title=title, section=section, body=body, lead=lead, dark=dark, cls=cls, toc=toc,
                      content_style=content_style))


def render_pages():
    out = []
    for i, p in enumerate(PAGES):
        n = i + 1
        if p.get("raw"):
            out.append(p["raw"](n))
            continue
        kicker = f"{n - 2:02d} — {p['section']}"
        lead = f'<p class="lead">{p["lead"]}</p>' if p["lead"] else ""
        dark = " page--dark" if p["dark"] else ""
        out.append(
            f'<section class="page{dark} {p["cls"]}" id="p{n}">'
            f'<header class="ph"><p class="ph__kicker">{kicker}</p><h2 class="ph__title">{p["title"]}</h2>'
            f'<span class="ph__rule"></span></header>{lead}'
            f'<div class="content" style="margin-top:7mm;{p["content_style"]}">{p["body"]}</div>'
            f'<footer class="pf"><span>Skill360 — Charte graphique · V1.0</span><span>{p["section"]}</span>'
            f'<span class="pf__num">{n:02d}</span></footer></section>')
    return "\n".join(out)


def raw_page(fn, title="", section="", toc=False):
    PAGES.append(dict(raw=fn, title=title, section=section, toc=toc))
