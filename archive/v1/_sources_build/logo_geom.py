"""Skill360 logo geometry: Unbounded glyph outlines + the 'Orbite' ring symbol.

All coordinates are in font units (UPM 1000), y axis pointing DOWN, baseline at y=0
(cap height therefore sits at y=-750).
"""
import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import RecordingPen, DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb


# --------------------------------------------------------------------------- fonts
class Font:
    def __init__(self, path, wght):
        self.path = path
        self.blob = open(path, "rb").read()
        self.tt = instantiateVariableFont(TTFont(path), {"wght": wght}, inplace=False)
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.wght = wght
        self.upm = self.tt["head"].unitsPerEm
        self.cap = self.tt["OS/2"].sCapHeight

    def shape(self, text, features=None):
        face = hb.Face(self.blob)
        font = hb.Font(face)
        font.set_variations({"wght": self.wght})
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, features or {"kern": True, "liga": False})
        return [(self.order[i.codepoint], p.x_advance, p.x_offset, p.y_offset)
                for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def contours(self, gname):
        """Return list of contours, each a list of pen ops, in font coords (y up)."""
        rp = DecomposingRecordingPen(self.gs)
        self.gs[gname].draw(rp)
        contours, cur = [], []
        for op, args in rp.value:
            cur.append((op, args))
            if op in ("closePath", "endPath"):
                contours.append(cur)
                cur = []
        if cur:
            contours.append(cur)
        return contours

    @staticmethod
    def contour_bounds(contour):
        pts = [p for op, args in contour for p in args]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return min(xs), min(ys), max(xs), max(ys)

    def contour_path(self, contour, dx=0, dy=0, scale=1.0):
        """SVG path for a contour, flipped to y-down, translated by (dx, dy)."""
        pen = SVGPathPen(self.gs, ntos=lambda v: fmt(v))
        tp = TransformPen(pen, (scale, 0, 0, -scale, dx, dy))
        for op, args in contour:
            getattr(tp, op)(*args)
        return pen.getCommands()

    def glyph_path(self, gname, dx=0, dy=0, scale=1.0):
        pen = SVGPathPen(self.gs, ntos=lambda v: fmt(v))
        tp = TransformPen(pen, (scale, 0, 0, -scale, dx, dy))
        self.gs[gname].draw(tp)
        return pen.getCommands()

    def glyph_bounds(self, gname):
        bp = BoundsPen(self.gs)
        self.gs[gname].draw(bp)
        return bp.bounds


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# --------------------------------------------------------------------------- vector helpers
def polar(cx, cy, r, deg):
    """Point at angle deg measured CLOCKWISE from 12 o'clock (screen coords, y down)."""
    a = math.radians(deg)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def tangent(deg):
    a = math.radians(deg)
    return (math.cos(a), math.sin(a))  # clockwise direction


def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def mul(a, k): return (a[0] * k, a[1] * k)
def norm(a):
    l = math.hypot(*a)
    return (a[0] / l, a[1] / l)


def line_intersect(p1, d1, p2, d2):
    det = d1[0] * (-d2[1]) - d1[1] * (-d2[0])
    if abs(det) < 1e-9:
        return None
    rx, ry = p2[0] - p1[0], p2[1] - p1[1]
    t = (rx * (-d2[1]) - ry * (-d2[0])) / det
    return (p1[0] + t * d1[0], p1[1] + t * d1[1])


def line_circle(p, d, c, r, near):
    """Intersection of line p + t d with circle (c, r), the one closest to `near`."""
    fx, fy = p[0] - c[0], p[1] - c[1]
    a = d[0] ** 2 + d[1] ** 2
    b = 2 * (fx * d[0] + fy * d[1])
    cc = fx ** 2 + fy ** 2 - r ** 2
    disc = b * b - 4 * a * cc
    if disc < 0:
        return near
    sq = math.sqrt(disc)
    sols = [(-b - sq) / (2 * a), (-b + sq) / (2 * a)]
    pts = [(p[0] + t * d[0], p[1] + t * d[1]) for t in sols]
    return min(pts, key=lambda q: (q[0] - near[0]) ** 2 + (q[1] - near[1]) ** 2)


def angle_of(c, p):
    """Clockwise angle from 12 o'clock of point p around center c, in degrees [0, 360)."""
    return math.degrees(math.atan2(p[0] - c[0], -(p[1] - c[1]))) % 360


# --------------------------------------------------------------------------- the Orbite
def orbit_cut(cx, cy, ro, ri, deg, gap, tip):
    """Both boundaries of a chevron cut at angle `deg`.

    Returns dict with 'A' (end of the segment before the cut, convex arrow point)
    and 'B' (start of the segment after the cut, concave notch); each holds
    outer point, tip point, inner point.
    """
    c = (cx, cy)
    rm = (ro + ri) / 2
    t = tangent(deg)
    o = polar(cx, cy, ro, deg)
    i = polar(cx, cy, ri, deg)
    tp = add(polar(cx, cy, rm, deg), mul(t, tip))
    e1 = norm(sub(tp, o))
    e2 = norm(sub(i, tp))
    # normals pointing forward (clockwise side)
    def fwd_normal(e):
        n = (-e[1], e[0])
        return n if n[0] * t[0] + n[1] * t[1] > 0 else (e[1], -e[0])
    n1, n2 = fwd_normal(e1), fwd_normal(e2)
    out = {}
    for side, k in (("A", -gap / 2), ("B", gap / 2)):
        p1 = add(o, mul(n1, k))
        p2 = add(tp, mul(n2, k))
        tip_pt = line_intersect(p1, e1, p2, e2) if tip > 1e-6 else add(tp, mul(t, k))
        if tip_pt is None:
            tip_pt = add(tp, mul(t, k))
        outer = line_circle(p1, e1, c, ro, add(o, mul(t, k)))
        inner = line_circle(p2, e2, c, ri, add(i, mul(t, k)))
        out[side] = (outer, tip_pt, inner)
    return out


def orbit_segments(cx, cy, ro, ri, cuts, gap, tip):
    """Closed SVG paths for each ring segment between consecutive cuts (clockwise)."""
    data = [orbit_cut(cx, cy, ro, ri, d, gap, tip) for d in cuts]
    c = (cx, cy)
    paths = []
    n = len(cuts)
    for k in range(n):
        b = data[k]["B"]            # start of this segment
        a = data[(k + 1) % n]["A"]  # end of this segment
        ob, tb, ib = b
        oa, ta, ia = a
        span_outer = (angle_of(c, oa) - angle_of(c, ob)) % 360
        span_inner = (angle_of(c, ia) - angle_of(c, ib)) % 360
        lo = 1 if span_outer > 180 else 0
        li = 1 if span_inner > 180 else 0
        d = (f"M{fmt(ob[0])} {fmt(ob[1])}"
             f"A{fmt(ro)} {fmt(ro)} 0 {lo} 1 {fmt(oa[0])} {fmt(oa[1])}"
             f"L{fmt(ta[0])} {fmt(ta[1])}"
             f"L{fmt(ia[0])} {fmt(ia[1])}"
             f"A{fmt(ri)} {fmt(ri)} 0 {li} 0 {fmt(ib[0])} {fmt(ib[1])}"
             f"L{fmt(tb[0])} {fmt(tb[1])}Z")
        paths.append(d)
    return paths, data


def circle_path(cx, cy, r):
    """A circle as a single closed path (two arcs), clockwise from 12 o'clock."""
    return (f"M{fmt(cx)} {fmt(cy - r)}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx)} {fmt(cy + r)}"
            f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx)} {fmt(cy - r)}Z")
