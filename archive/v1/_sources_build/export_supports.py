"""Generate HTML sources for every exported asset + a job list for render_jobs.js.

usage: python export_supports.py <scratch_dir> <deliverables_root>
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding="utf-8")
SCRATCH, ROOT = sys.argv[1], sys.argv[2]
sys.path.insert(0, SCRATCH)
from charte_lib import logo, rings, DATA, C


NUIT, INDIGO, ORBITE, HALO, FUMEE, CYAN = C["nuit"], C["indigo"], C["orbite"], C["halo"], C["fumee"], C["cyan"]
ARDOISE, BRUME = "#4A5170", "#A6AFCC"
GPOS = f"linear-gradient(165deg,{CYAN},{ORBITE})"
EXP = os.path.join(SCRATCH, "charte", "exports")
os.makedirs(EXP, exist_ok=True)
SPRITE = open(os.path.join(SCRATCH, "build", "sprite.svg"), encoding="utf-8").read()
ICONS = open(os.path.join(SCRATCH, "site_src", "icons.svg"), encoding="utf-8").read()
jobs = []

BASE_CSS = """
@font-face { font-family: "Unbounded"; src: url("../fonts/unbounded-var.woff2") format("woff2"); font-weight: 200 900; }
@font-face { font-family: "Manrope"; src: url("../fonts/manrope-var.woff2") format("woff2"); font-weight: 200 800; }
* { box-sizing: border-box; } html, body { margin: 0; padding: 0; }
body { font-family: Manrope, Arial, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
p { margin: 0; } .L { display: block; height: auto; overflow: visible; }
.rings { position: absolute; pointer-events: none; }
.rings circle { fill: none; stroke: rgba(238, 242, 250, .1); stroke-width: 1; vector-effect: non-scaling-stroke; }
.grad-neg { background: linear-gradient(165deg, #6FE0FF, #2F6BFF); -webkit-background-clip: text; background-clip: text; color: transparent; }
.v { font-weight: 700; color: #2F6BFF; }
"""


def doc(name, body, css="", page=None):
    pg = f"@page {{ size: {page}; margin: 0; }}" if page else ""
    html = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{BASE_CSS}{pg}{css}</style></head>'
            f'<body>{SPRITE}{ICONS}{body}</body></html>')
    path = os.path.join(EXP, name)
    open(path, "w", encoding="utf-8").write(html)
    return path


def out(*parts):
    p = os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


# ------------------------------------------------------------------ 02_Logo — PNG exports of every SVG
svgdir = os.path.join(SCRATCH, "build", "svg")
for f in sorted(os.listdir(svgdir)):
    if not f.endswith(".svg") or f in ("skill360-favicon.svg", "skill360-icone-app.svg"):
        continue
    vb = re.search(r'viewBox="([^"]+)"', open(os.path.join(svgdir, f), encoding="utf-8").read()).group(1).split()
    vw, vh = float(vb[2]), float(vb[3])
    W = 1000 if "orbite" in f else (1400 if "carre" in f else 2400)
    H = round(W * vh / vw)
    p = doc(f"logo_{f[:-4]}.html", f'<img src="../logos/{f}" style="display:block;width:{W}px;height:{H}px">')
    jobs.append(dict(html=p, out=out("02_Logo", "PNG", f[:-4] + ".png"), w=W, h=H, transparent=True))

# favicons & app icons
for size in (16, 32, 48, 64, 256):
    p = doc(f"fav_{size}.html", f'<img src="../logos/skill360-favicon.svg" style="display:block;width:{size}px;height:{size}px">')
    jobs.append(dict(html=p, out=out("02_Logo", "Favicon", f"favicon-{size}.png"), w=size, h=size))
for size, name in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png"), (1024, "icone-app-1024.png")):
    p = doc(f"app_{size}.html", f'<img src="../logos/skill360-icone-app.svg" style="display:block;width:{size}px;height:{size}px">')
    jobs.append(dict(html=p, out=out("02_Logo", "Favicon", name), w=size, h=size))

# ------------------------------------------------------------------ 05_Papeterie — print PDFs
card_css = """
.pg { position: relative; width: 91mm; height: 61mm; overflow: hidden; break-after: page; }
.trim { position: absolute; left: 3mm; top: 3mm; width: 85mm; height: 55mm; }
"""
recto = (f'<div class="pg" style="background:{NUIT}">'
         + rings(760, 520, [300, 400, 520], style="position:absolute;inset:0", sats=[(400, 300, 8, HALO)])
         + f'<div class="trim" style="display:grid;place-items:center">{logo("logo-h-neg", "56mm")}</div></div>')
verso = (f'<div class="pg" style="background:{FUMEE}"><div class="trim" style="padding:7mm">'
         f'<p style="font:500 9pt/1.1 Unbounded;letter-spacing:-.01em;color:{NUIT}">Prénom Nom</p>'
         f'<p style="margin-top:1.4mm;font:700 4.6pt/1.3 Manrope;letter-spacing:.2em;text-transform:uppercase;color:{ORBITE}">Fonction</p>'
         f'<span style="display:block;width:8mm;height:.8pt;background:{GPOS};margin:3.2mm 0"></span>'
         f'<p style="font:500 5.6pt/1.75 Manrope;color:{NUIT}">T. +33 (0)0 00 00 00 00<br>prenom.nom@skill360.fr<br><b>skill360.fr</b></p>'
         f'<div style="position:absolute;right:6mm;bottom:6mm">{logo("orbite", "9mm")}</div>'
         f'<p style="position:absolute;left:7mm;bottom:6.4mm;font:600 4.2pt/1 Manrope;letter-spacing:.18em;text-transform:uppercase;color:{ARDOISE}">Développer ses compétences à 360°</p>'
         f'</div></div>')
p = doc("carte-de-visite.html", recto + verso, card_css, "91mm 61mm")
jobs.append(dict(html=p, out=out("05_Papeterie", "Skill360_carte-de-visite_85x55_fond-perdu-3mm.pdf"), pdf=True))

lh_css = """
.pg { position: relative; width: 210mm; height: 297mm; overflow: hidden; break-after: page; background: #fff; }
.foot { position: absolute; left: 20mm; right: 20mm; bottom: 12mm; border-top: .5pt solid #D6DCEA; padding-top: 2.4mm;
        font: 500 6.5pt/1.55 Manrope; color: #4A5170; }
"""
sheet1 = (f'<div class="pg"><div style="position:absolute;left:20mm;top:18mm">{logo("logo-h", "45mm")}</div>'
          f'<div class="foot">Skill360 — [forme juridique] au capital de [montant] — [adresse du siège] — SIRET [numéro]<br>'
          f'Déclaration d\'activité enregistrée sous le n° [numéro] auprès du préfet de région [région]. Cet enregistrement ne vaut pas agrément de l\'État. — skill360.fr</div></div>')
sheet2 = f'<div class="pg"><div style="position:absolute;left:20mm;top:18mm">{logo("orbite", "8mm")}</div></div>'
p = doc("papier-en-tete.html", sheet1 + sheet2, lh_css, "210mm 297mm")
jobs.append(dict(html=p, out=out("05_Papeterie", "Skill360_papier-en-tete_A4.pdf"), pdf=True))

cert = (f'<div style="position:relative;width:297mm;height:210mm;overflow:hidden;background:{FUMEE};padding:19mm 23mm">'
        f'<div style="position:absolute;right:-42mm;top:-12mm;opacity:.06">{logo("orbite", "200mm", n360=NUIT)}</div>'
        f'<div style="position:relative">{logo("logo-h", "92mm")}</div>'
        f'<p style="position:relative;margin-top:19mm;font:400 27pt/1.05 Unbounded;letter-spacing:-.025em;color:{NUIT}">Attestation de<br>fin de formation</p>'
        f'<span style="display:block;width:25mm;height:2pt;background:{GPOS};margin:8mm 0"></span>'
        f'<p style="position:relative;font:500 11pt/1.6 Manrope;color:{ARDOISE}">délivrée à</p>'
        f'<p style="position:relative;font:500 21pt/1.2 Unbounded;letter-spacing:-.01em;color:{NUIT}">[Prénom Nom]</p>'
        f'<p style="position:relative;margin-top:5mm;font:500 11.5pt/1.7 Manrope;color:{NUIT}">pour avoir suivi la formation <b>« [Intitulé de la formation] »</b><br>'
        f'du [date] au [date] — durée&nbsp;: [nombre] heures — modalité&nbsp;: [présentiel / distanciel / mixte]<br>'
        f'Évaluation des acquis&nbsp;: [résultat]</p>'
        f'<div style="position:absolute;left:23mm;right:23mm;bottom:17mm;display:flex;justify-content:space-between;align-items:flex-end;font:600 9pt/1.5 Manrope;color:{ARDOISE}">'
        f'<span>Fait à [ville], le [date]</span><span style="border-top:.6pt solid {NUIT};padding-top:2mm;width:84mm;text-align:center">[Nom], responsable pédagogique</span></div></div>')
p = doc("attestation.html", cert, "", "297mm 210mm")
jobs.append(dict(html=p, out=out("05_Papeterie", "Skill360_attestation-fin-de-formation_A4-paysage.pdf"), pdf=True))

# ------------------------------------------------------------------ 06_Digital — social media + e-mail
def social(name, w, h, body, bg=NUIT):
    p = doc(name, f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{bg}">{body}</div>')
    return p


banner = social("li_banner.html", 1128, 191,
                rings(880, 500, [300, 420, 560], style="position:absolute;inset:0", sats=[(420, 250, 7, HALO)])
                + f'<p style="position:absolute;right:64px;top:50%;transform:translateY(-50%);font:700 15px/1 Manrope;letter-spacing:.3em;color:{HALO}">DÉVELOPPER SES COMPÉTENCES À 360°</p>')
jobs.append(dict(html=banner, out=out("06_Digital", "Reseaux_sociaux", "linkedin-banniere_1128x191.png"), w=1128, h=191))
av = doc("li_avatar.html", '<img src="../logos/skill360-icone-app.svg" style="display:block;width:400px;height:400px">')
jobs.append(dict(html=av, out=out("06_Digital", "Reseaux_sociaux", "avatar_400x400.png"), w=400, h=400))

post_dark = social("post_session.html", 1200, 1200,
                   rings(820, 820, [300, 420], style="position:absolute;inset:0")
                   + f'<div style="position:absolute;left:110px;top:110px;right:110px">'
                     f'<p style="font:700 30px/1 Manrope;letter-spacing:.24em;color:{HALO}">NOUVELLE SESSION</p>'
                     f'<p style="margin-top:44px;font:400 104px/1.08 Unbounded;letter-spacing:-.02em;color:{FUMEE}">[Intitulé<br>de la formation]</p>'
                     f'<p style="margin-top:44px;font:600 36px/1.4 Manrope;color:{BRUME}">[Durée] · [modalité] · [dates]</p></div>'
                   + f'<div style="position:absolute;left:110px;bottom:110px">{logo("logotype-neg", "330px")}</div>'
                   + f'<div style="position:absolute;right:110px;bottom:100px">{logo("orbite-neg", "140px")}</div>')
jobs.append(dict(html=post_dark, out=out("06_Digital", "Reseaux_sociaux", "post-session_1200x1200.png"), w=1200, h=1200))

post_light = social("post_conseil.html", 1200, 1200,
                    f'<div style="position:absolute;left:110px;top:110px;right:110px">'
                    f'<p style="font:700 30px/1 Manrope;letter-spacing:.24em;color:{ORBITE}">CONSEIL</p>'
                    f'<p style="margin-top:44px;font:400 92px/1.1 Unbounded;letter-spacing:-.02em;color:{NUIT}">[Votre conseil<br>en une phrase]</p></div>'
                    f'<div style="position:absolute;left:110px;bottom:110px">{logo("logotype", "330px")}</div>', bg=FUMEE)
jobs.append(dict(html=post_light, out=out("06_Digital", "Reseaux_sociaux", "post-conseil_1200x1200.png"), w=1200, h=1200))

post_quote = social("post_parcours.html", 1200, 1200,
                    f'<div style="position:absolute;left:110px;top:110px;right:110px">'
                    f'<p style="font:700 30px/1 Manrope;letter-spacing:.24em;color:{HALO}">PARCOURS</p>'
                    f'<p style="margin-top:44px;font:300 76px/1.25 Unbounded;color:{FUMEE}">« [Citation de l\'apprenant, publiée avec son accord écrit] »</p>'
                    f'<p style="margin-top:40px;font:600 34px/1.4 Manrope;color:{BRUME}">[Prénom], [formation suivie]</p></div>'
                    f'<div style="position:absolute;right:110px;bottom:100px">{logo("orbite-neg", "140px")}</div>', bg=INDIGO)
jobs.append(dict(html=post_quote, out=out("06_Digital", "Reseaux_sociaux", "post-parcours_1200x1200.png"), w=1200, h=1200))

story = social("story.html", 1080, 1920,
               rings(500, 760, [260, 360, 470], style="position:absolute;inset:0")
               + f'<div style="position:absolute;left:100px;top:250px">{logo("logotype-neg", "420px")}</div>'
               + f'<p style="position:absolute;left:100px;right:100px;top:760px;font:400 118px/1.08 Unbounded;letter-spacing:-.02em;color:{FUMEE}">[Inscriptions ouvertes]</p>'
               + f'<p style="position:absolute;left:100px;top:1100px;font:600 40px/1.4 Manrope;color:{BRUME}">[Sessions de janvier]</p>'
               + f'<div style="position:absolute;left:100px;right:100px;bottom:300px;height:120px;border-radius:60px;background:#2D69FC;display:grid;place-items:center;font:700 40px/1 Manrope;color:#fff">En savoir plus</div>')
jobs.append(dict(html=story, out=out("06_Digital", "Reseaux_sociaux", "story_1080x1920.png"), w=1080, h=1920))

sig_icon = doc("sig_icon.html", f'<div style="width:120px;height:120px;border-radius:12px;background:{NUIT};display:grid;place-items:center">{logo("orbite-neg", "76px")}</div>')
jobs.append(dict(html=sig_icon, out=out("06_Digital", "Signature_e-mail", "signature-orbite_120.png"), w=120, h=120, transparent=True))

signature = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Signature e-mail Skill360</title></head>
<body style="margin:0;padding:24px;background:#ffffff">
<!-- Signature e-mail Skill360 — tableau HTML, styles en ligne, Arial (les polices de marque ne se chargent pas dans les messageries).
     Avant déploiement : héberger signature-orbite_120.png sur un serveur HTTPS et remplacer l'attribut src par son URL absolue. -->
<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="max-width:480px;font-family:Arial,Helvetica,sans-serif;color:#070B1F;border-collapse:collapse">
  <tr><td colspan="2" style="padding:0 0 16px 0;font-size:14px;line-height:20px">Bien cordialement,</td></tr>
  <tr>
    <td valign="top" style="padding:0 16px 0 0;width:60px">
      <img src="signature-orbite_120.png" width="60" height="60" alt="Skill360" style="display:block;border:0;border-radius:6px">
    </td>
    <td valign="top" style="padding:0 0 0 16px;border-left:1px solid #D6DCEA">
      <div style="font-size:15px;line-height:20px;font-weight:bold;color:#070B1F">Prénom Nom</div>
      <div style="font-size:10px;line-height:16px;font-weight:bold;letter-spacing:1.5px;color:#2F6BFF;text-transform:uppercase">Fonction · Skill360</div>
      <div style="width:28px;height:2px;background:#2F6BFF;margin:10px 0;line-height:2px;font-size:0">&nbsp;</div>
      <div style="font-size:12px;line-height:19px;color:#070B1F">
        T. <a href="tel:+33000000000" style="color:#070B1F;text-decoration:none">+33 (0)0 00 00 00 00</a><br>
        <a href="mailto:prenom.nom@skill360.fr" style="color:#070B1F;text-decoration:none">prenom.nom@skill360.fr</a><br>
        <a href="https://skill360.fr" style="color:#070B1F;text-decoration:none;font-weight:bold">skill360.fr</a>
      </div>
      <div style="font-size:11px;line-height:16px;color:#4A5170;padding-top:8px">Développer ses compétences à 360°.</div>
    </td>
  </tr>
</table>
</body></html>
"""
open(out("06_Digital", "Signature_e-mail", "signature-email_skill360.html"), "w", encoding="utf-8").write(signature)

# ------------------------------------------------------------------ 07_Site_Web — share image
og = social("og_image.html", 1200, 630,
            '<div style="position:absolute;inset:0;background:radial-gradient(80% 90% at 50% 40%,#10184A 0%,#070B1F 70%)"></div>'
            + rings(500, 470, [200, 290, 390, 500], style="position:absolute;inset:0", sats=[(290, 52, 5, HALO), (500, 236, 6, ORBITE)])
            + f'<div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%)">{logo("logo-h-neg", "760px")}</div>'
            + f'<p style="position:absolute;left:0;right:0;bottom:90px;text-align:center;font:500 34px/1 Unbounded;letter-spacing:-.01em;color:{FUMEE}">Développer ses compétences <span class="grad-neg">à 360°</span>.</p>')
jobs.append(dict(html=og, out=os.path.join(SCRATCH, "site_src", "assets", "img", "og-image.png"), w=1200, h=630))
os.makedirs(os.path.join(SCRATCH, "site_src", "assets", "img"), exist_ok=True)
for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png")):
    src = "skill360-favicon.svg" if size == 32 else "skill360-icone-app.svg"
    p = doc(f"site_{name}.html", f'<img src="../logos/{src}" style="display:block;width:{size}px;height:{size}px">')
    jobs.append(dict(html=p, out=os.path.join(SCRATCH, "site_src", "assets", "img", name), w=size, h=size))

json.dump(jobs, open(os.path.join(EXP, "jobs.json"), "w", encoding="utf-8"), indent=1)
print("jobs:", len(jobs))
