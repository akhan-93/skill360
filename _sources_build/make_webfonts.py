"""Subset the variable fonts to Latin and save them as WOFF2.
usage: python make_webfonts.py <fonts_dir> <out_dir>
"""
import sys, os
from fontTools import subset
from fontTools.ttLib import TTFont

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
UNICODES = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
            "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2192,U+2190,U+2212,U+2215,U+2248,U+2264,U+2265,"
            "U+00B0,U+2116,U+FEFF,U+FFFD")
for name, file in (("unbounded", "Unbounded-VF.ttf"), ("manrope", "Manrope-VF.ttf")):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    font = TTFont(os.path.join(src, file))
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=subset.parse_unicodes(UNICODES))
    sub.subset(font)
    dst = os.path.join(out, f"{name}-var.woff2")
    font.flavor = "woff2"
    font.save(dst)
    print(dst, os.path.getsize(dst))
