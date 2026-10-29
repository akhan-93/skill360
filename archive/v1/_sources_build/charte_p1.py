"""Charte Skill360 — partie I : couverture, sommaire, fondations, identité, système."""
import math
from charte_lib import *
from logo_geom import polar, fmt

NUIT, INDIGO, ORBITE, HALO, FUMEE, CYAN = C["nuit"], C["indigo"], C["orbite"], C["halo"], C["fumee"], C["cyan"]
ARDOISE, BRUME = "#4A5170", "#A6AFCC"
S = DATA["symbol"]
SCX, SCY = S["cx"], S["cy"]
R = DATA["D"] / 2
RI = R - DATA["T"]
U = DATA["unit"]


# =================================================================== 01 couverture
def cover(n):
    return (f'<section class="page cover" id="p{n}">'
            + rings(500, 470, [190, 270, 370, 490, 640], style="position:absolute",
                    sats=[(270, 52, 5, HALO), (490, 236, 6, ORBITE), (370, 312, 3.5, FUMEE), (640, 120, 4, HALO)])
            + '<div class="halo" style="width:190mm;height:190mm;left:53.5mm;top:-11mm"></div>'
            + f'<div class="cover__logo">{logo("logo-h-neg", "168mm")}</div>'
            + '<div class="cover__foot"><div><p class="cover__title">Charte graphique</p>'
              '<p class="cover__meta">Brand identity guidelines · Version 1.0 · 2026</p></div>'
              '<div class="cover__sig">Développer ses compétences à 360°<span>Centre de formation</span></div></div>'
            + '</section>')


raw_page(cover, "Couverture", "")


# =================================================================== 02 sommaire
def toc(n):
    groups = [("I — Fondations et identité", 3, 22), ("II — Applications", 23, 38), ("Annexes", 39, 41)]
    cols = [[], []]
    for gi, (name, a, b) in enumerate(groups):
        rows = "".join(
            f'<div class="toc__row"><i>{k:02d}</i><span>{PAGES[k - 1]["title"]}</span><em>{PAGES[k - 1]["section"]}</em></div>'
            for k in range(a, b + 1))
        cols[0 if gi == 0 else 1].append(f'<div style="margin-bottom:6mm"><p class="toc__h">{name}</p>{rows}</div>')
    return (f'<section class="page" id="p{n}"><header class="ph"><p class="ph__kicker">Sommaire</p>'
            f'<h2 class="ph__title">Table des matières</h2><span class="ph__rule"></span></header>'
            f'<div class="toc" style="margin-top:8mm"><div>{"".join(cols[0])}</div><div>{"".join(cols[1])}</div></div>'
            f'<footer class="pf"><span>Skill360 — Charte graphique · V1.0</span><span>Sommaire</span>'
            f'<span class="pf__num">{n:02d}</span></footer></section>')


raw_page(toc, "Sommaire", "")

# =================================================================== 03 plateforme
page("Plateforme de marque", "Marque", f"""
<div class="g g2" style="gap:16mm">
  <div>
    {blk("Signature", '<p class="big" style="font-size:17pt">Développer ses compétences <span class="grad">à&nbsp;360°</span>.</p>')}
    {blk("Baseline du logotype", '<p class="mid" style="font-size:9pt;letter-spacing:.14em;text-transform:uppercase;font-family:var(--t);font-weight:600">Formation &amp; développement des compétences</p>')}
    {blk("Promesse", txt("<b>Chaque parcours part de la personne.</b> Skill360 réunit savoir, savoir-faire et savoir-être pour que chaque apprenant fasse le tour complet de sa compétence — et en ressorte grandi."))}
    {blk("Concept", txt("L'apprenant est au centre, les compétences gravitent autour de lui comme une orbite. Le halo de fumée blanche évoque le mouvement et la transformation&nbsp;: <i>on entre dans l'orbite, on en ressort grandi.</i>"))}
  </div>
  <div>
    {blk("Positionnement", txt("Skill360 est un centre de formation pluridisciplinaire. Il accompagne salariés, entreprises, demandeurs d'emploi et indépendants dans le développement de leurs compétences techniques, transversales et comportementales — en présentiel, à distance ou en format mixte.") + txt("Skill360 ne vend pas un catalogue&nbsp;: il construit des parcours."))}
    {blk("Mission", txt("Rendre chaque apprenant capable d'agir&nbsp;: transmettre des savoirs, entraîner des savoir-faire, faire grandir des savoir-être."))}
    {blk("Vision 2030", txt("Devenir une référence de la formation à 360°, où chaque parcours se construit autour de la personne, pas autour du programme."))}
    {blk("Publics", txt("Salariés, entreprises, demandeurs d'emploi, indépendants. <b>Tous profils, tous parcours.</b>"))}
  </div>
</div>
<div style="margin-top:9mm;display:grid;grid-template-columns:auto 1fr 1fr 1fr;gap:8mm;align-items:center;padding:5mm 7mm;border-radius:1.6mm;background:var(--nuit);color:var(--fumee)">
  {logo("orbite-neg", "15mm")}
  <div><p style="font:500 9.5pt/1.2 var(--d)">Savoir</p><p class="sm" style="color:var(--brume);margin-top:1mm">Les connaissances qui fondent une expertise.</p></div>
  <div><p style="font:500 9.5pt/1.2 var(--d)">Savoir-faire</p><p class="sm" style="color:var(--brume);margin-top:1mm">La pratique, les cas réels, les outils en main.</p></div>
  <div><p style="font:500 9.5pt/1.2 var(--d)">Savoir-être</p><p class="sm" style="color:var(--brume);margin-top:1mm">La posture qui transforme une compétence en impact.</p></div>
</div>""")

# =================================================================== 04 valeurs, ton, méthode
values = [("Exploration", "Oser de nouveaux horizons"), ("Excellence", "Des formations exigeantes"),
          ("Accompagnement", "Personne n'est laissé seul"), ("Ouverture", "Tous profils, tous parcours")]
steps = [("01", "Positionner", "Un diagnostic de départ&nbsp;: acquis, objectifs, contraintes."),
         ("02", "Construire", "Un parcours sur mesure&nbsp;: contenus, rythme, format."),
         ("03", "Former", "Des formateurs praticiens, une pédagogie active."),
         ("04", "Valoriser", "Évaluation des acquis, attestation, suivi à froid.")]
page("Valeurs, ton et méthode", "Marque", f"""
<div class="g" style="grid-template-columns:1.75fr 1fr;gap:14mm">
  <div>
    {lbl("Valeurs")}
    <div class="g g4 gap-s">{"".join(f'<div class="card-b"><h4>{a}</h4><p>{b}</p></div>' for a, b in values)}</div>
    <div style="margin-top:8mm">{lbl("La méthode Skill360")}
      <div class="g g4 gap-s">{"".join(f'<div class="step-c"><i>{a}</i><h4>{b}</h4><p>{c}</p></div>' for a, b, c in steps)}</div>
    </div>
    <div style="margin-top:8mm">{note("À compléter avant diffusion externe", f"Raison sociale, forme juridique, SIRET, numéro de déclaration d'activité, certification qualité et catalogue définitif&nbsp;: {V}. Ces données se reprennent des documents officiels, jamais de cette charte.")}</div>
  </div>
  <div>
    {blk("Ton", '<p class="mid">Inspirant, clair, bienveillant.</p>' + txt("On tutoie l'ambition, pas l'apprenant&nbsp;: Skill360 vouvoie toujours. Phrases courtes, verbes d'action, exemples concrets.", "mut"))}
    {blk("Personnalité", txt("Lumineuse, moderne, exigeante, chaleureuse, en mouvement."))}
    {blk("La marque évite", bul(["Le jargon pédagogique et les sigles non expliqués", "Les promesses miracles («&nbsp;devenez expert en deux jours&nbsp;»)", "Les codes scolaires&nbsp;: tableau noir, toque, pomme, crayon", "Les superlatifs invérifiables («&nbsp;n°&nbsp;1&nbsp;», «&nbsp;100&nbsp;% de réussite&nbsp;»)"], "bul--x"))}
  </div>
</div>""")

# =================================================================== 05 logotype
page("Le logotype", "Identité", f"""
<div class="g g3 gap-s" style="grid-template-rows:auto auto">
  <div style="grid-column:span 2">{lbl("Version principale — avec signature")}{tile(logo("logo-h", "112mm"), "fumee", "54mm", cap="Signature par défaut de tous les supports.")}</div>
  <div>{lbl("Version carrée")}{tile(logo("logo-sq", "44mm"), "fumee", "54mm", cap="Formats carrés et étroits&nbsp;: avatars, affiches, signalétique.")}</div>
  <div>{lbl("Logotype seul")}{tile(logo("logotype", "60mm"), "blanc", "36mm", cap="Petites tailles, ou quand la signature figure déjà sur le support.")}</div>
  <div>{lbl("Symbole seul — l'Orbite")}{tile(logo("orbite", "21mm"), "blanc", "36mm", cap="Avatar, favicon, icône d'application, marquage.")}</div>
  <div>{lbl("Sur Nuit spatiale")}{tile(logo("logo-h-neg", "66mm"), "nuit", "36mm", cap="Version de référence sur fond sombre.")}</div>
</div>""", lead="Quatre verrouillages officiels, fournis en fichiers vectoriels. Le logotype est composé en Unbounded&nbsp;; seul le zéro est dessiné. Aucune autre composition n'est admise.")

# =================================================================== 06 symbole
sym_tile = (f'<div class="tile tile--nuit" style="height:118mm;width:118mm">'
            + rings(500, 500, [330, 400, 470], style="position:absolute")
            + '<div class="halo" style="width:110mm;height:110mm;left:4mm;top:4mm"></div>'
            + logo("orbite-neg", "64mm", style="position:relative") + '</div>')
page("Le symbole — l'Orbite", "Identité", f"""
<div class="g" style="grid-template-columns:118mm 1fr;gap:14mm;margin-top:-2mm">
  {sym_tile}
  <div style="padding-top:2mm">
    {blk("L'Orbite", txt("Le zéro de 360 devient une orbite&nbsp;: un tour complet. C'est le seul dessin propre à la marque&nbsp;; tout le reste du logotype est composé en Unbounded."))}
    {blk("Trois segments", txt("<b>Savoir, savoir-faire, savoir-être</b>&nbsp;: les trois dimensions de la compétence. Trois arcs égaux de 120°&nbsp;; aucun ne domine les autres."))}
    {blk("Le chevron", txt("Chaque coupe est une flèche orientée dans le sens horaire&nbsp;: les segments se poussent l'un l'autre. L'Orbite ne tourne que dans ce sens — celui de la progression."))}
    {blk("Le point", txt("Le point du i est l'apprenant. Il porte la couleur du 360&nbsp;: il est déjà en orbite. Quand l'Orbite est utilisée seule, <b>le point reprend sa place au centre</b>."))}
    {blk("Le dégradé", txt("Du cyan au bleu, du haut vers le bas&nbsp;: la lumière vient d'en haut. Le dégradé n'appartient qu'au «&nbsp;360&nbsp;» et au point — jamais à «&nbsp;Skill&nbsp;»."))}
  </div>
</div>""")


# =================================================================== 07 construction
def construction_svg():
    pad_l, pad_r, pad_t, pad_b = 540, 1460, 650, 480
    vb =f"{fmt(SCX - pad_l)} {fmt(SCY - pad_t)} {fmt(pad_l + pad_r)} {fmt(pad_t + pad_b)}"
    g = []
    # grid 100 x 100 U, step 10 U
    for k in range(11):
        v = -R + k * 80
        g.append(f'<line x1="{fmt(SCX - R)}" y1="{fmt(SCY + v)}" x2="{fmt(SCX + R)}" y2="{fmt(SCY + v)}"/>')
        g.append(f'<line x1="{fmt(SCX + v)}" y1="{fmt(SCY - R)}" x2="{fmt(SCX + v)}" y2="{fmt(SCY + R)}"/>')
    grid = f'<g stroke="#D5DBEA" stroke-width="2.4">{"".join(g)}</g>'
    # cut guides
    guides = []
    for d in DATA["cuts"]:
        p = polar(SCX, SCY, R + 120, d)
        guides.append(f'<line x1="{fmt(SCX)}" y1="{fmt(SCY)}" x2="{fmt(p[0])}" y2="{fmt(p[1])}"/>')
    guides = f'<g stroke="{ARDOISE}" stroke-width="2.6" stroke-dasharray="14 10">{"".join(guides)}</g>'
    segs = "".join(f'<path d="{s}" fill="#DCE4F7" stroke="{NUIT}" stroke-width="3"/>' for s in S["segs"])
    dot = f'<path d="{S["dot"]}" fill="#DCE4F7" stroke="{NUIT}" stroke-width="3"/>'
    T = 'font-family="Manrope" font-weight="700" fill="#070B1F" font-size="33"'
    Tm = 'font-family="Manrope" font-weight="500" fill="#4A5170" font-size="30"'
    a = []
    # diameter
    yy = SCY - R - 110
    a.append(f'<g stroke="{ORBITE}" stroke-width="3"><line x1="{fmt(SCX - R)}" y1="{fmt(yy)}" x2="{fmt(SCX + R)}" y2="{fmt(yy)}"/>'
             f'<line x1="{fmt(SCX - R)}" y1="{fmt(yy - 22)}" x2="{fmt(SCX - R)}" y2="{fmt(yy + 22)}"/>'
             f'<line x1="{fmt(SCX + R)}" y1="{fmt(yy - 22)}" x2="{fmt(SCX + R)}" y2="{fmt(yy + 22)}"/></g>'
             f'<text x="{fmt(SCX)}" y="{fmt(yy - 30)}" text-anchor="middle" {T}>Ø 100 U</text>')
    # ring thickness (left)
    yy = SCY + 60
    a.append(f'<g stroke="{ORBITE}" stroke-width="3"><line x1="{fmt(SCX - R)}" y1="{fmt(yy)}" x2="{fmt(SCX - RI)}" y2="{fmt(yy)}"/>'
             f'<line x1="{fmt(SCX - R)}" y1="{fmt(yy - 18)}" x2="{fmt(SCX - R)}" y2="{fmt(yy + 18)}"/>'
             f'<line x1="{fmt(SCX - RI)}" y1="{fmt(yy - 18)}" x2="{fmt(SCX - RI)}" y2="{fmt(yy + 18)}"/></g>'
             f'<text x="{fmt(SCX - (R + RI) / 2)}" y="{fmt(yy + 52)}" text-anchor="middle" {T}>24 U</text>')
    # 120° arc
    ra = R + 70
    p1, p2 = polar(SCX, SCY, ra, DATA["cuts"][0] + 4), polar(SCX, SCY, ra, DATA["cuts"][1] - 4)
    pm = polar(SCX, SCY, ra + 50, (DATA["cuts"][0] + DATA["cuts"][1]) / 2)
    a.append(f'<path d="M{fmt(p1[0])} {fmt(p1[1])}A{ra} {ra} 0 0 1 {fmt(p2[0])} {fmt(p2[1])}" fill="none" stroke="{ORBITE}" stroke-width="3"/>'
             f'<text x="{fmt(pm[0])}" y="{fmt(pm[1])}" {T}>120°</text>')
    # callouts on the right
    callouts = []
    from logo_geom import orbit_cut
    c15 = orbit_cut(SCX, SCY, R, RI, DATA["cuts"][0], DATA["gap"], DATA["tip"])
    c135 = orbit_cut(SCX, SCY, R, RI, DATA["cuts"][1], DATA["gap"], DATA["tip"])
    tipA = c15["A"][1]
    gapM = ((c135["A"][1][0] + c135["B"][1][0]) / 2, (c135["A"][1][1] + c135["B"][1][1]) / 2)
    lx = SCX + R + 260
    items = [
        (tipA, SCY - 300, "Chevron — pointe avancée de 11 U", "sens horaire, coupe à 15°"),
        ((SCX + R, SCY), SCY - 70, "Coupes tous les 120°", "15° · 135° · 255°"),
        (gapM, SCY + 170, "Échappement — 6 U", "constant sur toute la coupe"),
        ((SCX + DATA["dot"] / 2 * .7, SCY + DATA["dot"] / 2 * .7), SCY + 380, "Point — Ø 28 U", "centré, comme le point du i"),
    ]
    for (px, py), ty, t1, t2 in items:
        callouts.append(f'<circle cx="{fmt(px)}" cy="{fmt(py)}" r="9" fill="{ORBITE}"/>'
                        f'<polyline points="{fmt(px)},{fmt(py)} {fmt(lx - 40)},{fmt(ty)} {fmt(lx - 10)},{fmt(ty)}" fill="none" stroke="{ORBITE}" stroke-width="2.6"/>'
                        f'<text x="{fmt(lx)}" y="{fmt(ty + 4)}" {T}>{t1}</text>'
                        f'<text x="{fmt(lx)}" y="{fmt(ty + 44)}" {Tm}>{t2}</text>')
    return (f'<svg viewBox="{vb}" style="width:100%;height:auto;display:block">{grid}{guides}{segs}{dot}'
            f'{"".join(a)}{"".join(callouts)}</svg>')


def logotype_guides_svg():
    lb = DATA["logo_bounds"]
    vb = f"{fmt(lb[0] - 900)} {fmt(lb[1] - 120)} {fmt(lb[2] - lb[0] + 1000)} {fmt(lb[3] - lb[1] + 220)}"
    lines = [(0, "Ligne de base"), (-566, "Hauteur d'x"), (-750, "Capitales"), (-375, "Axe de l'Orbite")]
    g = []
    for y, t in lines:
        dash = ' stroke-dasharray="20 14"' if y == -375 else ""
        g.append(f'<line x1="{fmt(lb[0] - 40)}" y1="{y}" x2="{fmt(lb[2] + 40)}" y2="{y}" stroke="{ORBITE if y == -375 else ARDOISE}" stroke-width="5"{dash}/>'
                 f'<text x="{fmt(lb[0] - 70)}" y="{y + 26}" text-anchor="end" font-family="Manrope" font-weight="700" font-size="74" fill="#4A5170">{t}</text>')
    x, y, w, h = DATA["viewbox_h"].split()
    return (f'<svg viewBox="{vb}" style="width:100%;height:auto;display:block">'
            f'<use href="#logotype" x="{x}" y="{y}" width="{w}" height="{h}" style="--lskill:#C9D2EA;--l360:#BBD3FB"/>'
            f'{"".join(g)}</svg>')


page("Construction", "Identité", f"""
<div class="g" style="grid-template-columns:152mm 1fr;gap:10mm;margin-top:-4mm">
  <div>{construction_svg()}</div>
  <div>
    {lbl("Cotes")}
    {tbl([["Grille", "100 × 100 U — 1 U = 1 % du diamètre"],
          ["Anneau", "épaisseur 24 U, Ø intérieur 52 U"],
          ["Coupes", "trois, tous les 120° (15°, 135°, 255°)"],
          ["Échappement", "6 U, identique au point du i"],
          ["Chevron", "pointe avancée de 11 U, sens horaire"],
          ["Point", "Ø 28 U"],
          ["Logotype", "Unbounded ExtraBold (800), approche −24/1000"],
          ["Signature", "Manrope SemiBold, capitales, justifiée sur la largeur du logotype"]], widths=["26%", "74%"])}
    <div style="margin-top:6mm">{lbl("Le logotype et l'Orbite")}{logotype_guides_svg()}</div>
    <p class="cap" style="margin-top:3mm">L'Orbite est centrée sur la mi-hauteur des capitales et déborde légèrement en haut et en bas, comme toute lettre ronde. Elle ne se redessine pas&nbsp;: elle s'utilise depuis les fichiers fournis.</p>
  </div>
</div>""", lead="")


# =================================================================== 08 zone de protection
def protection_svg():
    b = DATA["logo_tag_bounds"]
    X = DATA["dot"]
    m = X + 160
    vb = f"{fmt(b[0] - m)} {fmt(b[1] - m)} {fmt(b[2] - b[0] + 2 * m)} {fmt(b[3] - b[1] + 2 * m)}"
    zx, zy, zw, zh = b[0] - X, b[1] - X, b[2] - b[0] + 2 * X, b[3] - b[1] + 2 * X
    x, y, w, h = DATA["viewbox_ht"].split()
    dot = [l for l in DATA["letters"] if l["name"] == "dot"][0]
    dcx, dcy = dot["center"]
    # X markers on the four sides, between the logo and the protection line
    marks = [(zx, b[1] + (b[3] - b[1]) / 2 - X / 2), (b[2], b[1] + (b[3] - b[1]) / 2 - X / 2),
             ((b[0] + b[2]) / 2 - X / 2, zy), ((b[0] + b[2]) / 2 - X / 2, b[3])]
    xm = "".join(f'<rect x="{fmt(mx)}" y="{fmt(my)}" width="{X}" height="{X}" fill="#2F6BFF" fill-opacity=".14"/>'
                 f'<text x="{fmt(mx + X / 2)}" y="{fmt(my + X / 2 + 34)}" text-anchor="middle" font-family="Unbounded" font-weight="500" font-size="96" fill="#2F6BFF">X</text>'
                 for mx, my in marks)
    return (f'<svg viewBox="{vb}" style="width:100%;height:auto;display:block">'
            f'<rect x="{fmt(zx)}" y="{fmt(zy)}" width="{fmt(zw)}" height="{fmt(zh)}" fill="#fff" stroke="{ORBITE}" stroke-width="7" stroke-dasharray="28 18"/>'
            f'{xm}'
            f'<rect x="{fmt(b[0])}" y="{fmt(b[1])}" width="{fmt(b[2] - b[0])}" height="{fmt(b[3] - b[1])}" fill="none" stroke="#B9C3DD" stroke-width="4"/>'
            f'<use href="#logo-h" x="{x}" y="{y}" width="{w}" height="{h}"/>'
            f'<circle cx="{fmt(dcx)}" cy="{fmt(dcy)}" r="{X / 2 + 14}" fill="none" stroke="{ORBITE}" stroke-width="6"/>'
            f'<text x="{fmt(dcx)}" y="{fmt(b[1] - X - 40)}" text-anchor="middle" font-family="Manrope" font-weight="700" font-size="86" fill="#2F6BFF">X = Ø du point</text>'
            f'</svg>')


page("Zone de protection", "Identité", f"""
<div class="g" style="grid-template-columns:150mm 1fr;gap:12mm">
  <div class="tile tile--fumee" style="padding:9mm 8mm;display:block;place-items:normal">{protection_svg()}</div>
  <div>
    {blk("Définition", txt("<b>X = le diamètre du point du i.</b> La réserve vaut X sur les quatre côtés, mesurée depuis l'enveloppe du logotype — point et Orbite compris."))}
    {blk("Selon le verrouillage", tbl([["Principale", "X autour du bloc logotype + signature"], ["Logotype seul", "X sur les quatre côtés"], ["Carrée", "X autour des deux lignes"], ["Orbite seule", "X = Ø du point central"]], widths=["38%", "62%"]))}
    {blk("Cas particuliers", txt("Signalétique, enseigne et stands&nbsp;: la réserve passe à <b>2X</b>, la distance du regard réduisant la séparation perçue. Co-signature avec un partenaire ou un label&nbsp;: voir page 38."))}
  </div>
</div>""", lead="Aucun texte, image, filet ou bord de support ne pénètre la zone de réserve. Elle est proportionnelle, jamais fixée en millimètres.")

# =================================================================== 09 tailles minimales
fav = (f'<div style="display:flex;gap:5mm;align-items:center">'
       f'<img src="logos/skill360-favicon.svg" style="width:8.5mm;height:8.5mm;border-radius:1.2mm">'
       f'<img src="logos/skill360-favicon.svg" style="width:4.3mm;height:4.3mm;border-radius:.6mm"></div>')
page("Tailles minimales", "Identité", f"""
<div class="g g3 gap-s">
  <div>{lbl("Impression — principale")}{tile(logo("logo-h", "60mm"), "blanc", "30mm", cap="Largeur minimale <b>60 mm</b> (signature lisible).")}</div>
  <div>{lbl("Impression — logotype seul")}{tile(logo("logotype", "25mm"), "blanc", "30mm", cap="Largeur minimale <b>25 mm</b>.")}</div>
  <div>{lbl("Impression — Orbite")}{tile(logo("orbite", "6mm"), "blanc", "30mm", cap="Diamètre minimal <b>6 mm</b>.")}</div>
  <div>{lbl("Écran — principale")}{tile(logo("logo-h", "66mm"), "fumee", "30mm", cap="Largeur minimale <b>360 px</b> (représentée réduite).")}</div>
  <div>{lbl("Écran — logotype seul")}{tile(logo("logotype", "26.5mm"), "fumee", "30mm", cap="Largeur minimale <b>100 px</b>.")}</div>
  <div>{lbl("Favicon")}{tile(fav, "fumee", "30mm", cap="<b>32 et 16 px</b> — Orbite aplat Halo cyan sur carré Nuit spatiale.")}</div>
</div>
<div class="note" style="margin-top:7mm">Sous 60 mm (360 px), la signature devient illisible&nbsp;: on passe au logotype seul. Sous 32 px, le dégradé et les échappements ne se distinguent plus&nbsp;: on utilise l'Orbite en aplat. Sous 16 px, aucune version n'est garantie.</div>""",
     lead="En dessous de ces seuils, le verrouillage devient illisible&nbsp;: on passe à la version inférieure.")

# =================================================================== 10 monochromes
page("Monochromes et aplat", "Identité", f"""
<div class="g g5 gap-s">
  <div>{lbl("Aplat")}{tile(logo("logo-sq", "34mm", n360=ORBITE), "blanc", "46mm")}</div>
  <div>{lbl("Aplat négatif")}{tile(logo("logo-sq-neg", "34mm", n360=HALO), "nuit", "46mm")}</div>
  <div>{lbl("Nuit spatiale")}{tile(logo("logo-sq", "34mm", n360=NUIT), "blanc", "46mm")}</div>
  <div>{lbl("Noir")}{tile(logo("logo-sq", "34mm", skill="#000", n360="#000"), "blanc", "46mm")}</div>
  <div>{lbl("Blanc")}{tile(logo("logo-sq-neg", "34mm", n360="#fff", skill="#fff"), "indigo", "46mm")}</div>
</div>
<div class="g g3" style="margin-top:8mm;gap:10mm">
  {blk("Règle", txt("En une couleur, le «&nbsp;360&nbsp;» prend la couleur de «&nbsp;Skill&nbsp;». Ce sont les <b>échappements</b> de l'Orbite qui la font lire&nbsp;: ils ne se comblent jamais."))}
  {blk("Aplat", txt("Quand le dégradé n'est pas reproductible (sérigraphie, broderie, gravure, petits formats), le «&nbsp;360&nbsp;» passe en Bleu orbite plein — en Halo cyan sur fond sombre."))}
  {blk("Interdit", txt("Tramer le dégradé, le simuler en plusieurs teintes ou en dégradé radial. Une trame se bouche à l'impression et disparaît à la broderie."))}
</div>""", lead="Gravure, tampon, broderie, sérigraphie, marquage objet, documents en une couleur.")

# =================================================================== 11 fonds sombres
photo_dark = ("background:radial-gradient(60% 80% at 28% 30%, #2A3566 0%, transparent 60%),"
              "radial-gradient(50% 60% at 80% 75%, #1B2E5C 0%, transparent 60%),"
              "linear-gradient(160deg, #141B38, #05070F);")
photo_light = ("background:radial-gradient(60% 70% at 70% 30%, #FFFFFF 0%, transparent 60%),"
               "radial-gradient(55% 60% at 20% 80%, #D7DEEC 0%, transparent 60%),"
               "linear-gradient(160deg, #EEF1F7, #DFE5F0);")
page("Fonds sombres", "Identité", f"""
<div class="g g4 gap-s">
  <div>{lbl("Nuit spatiale — référence")}{tile(logo("logo-sq-neg", "38mm"), "nuit", "52mm", cap="«&nbsp;Skill&nbsp;» Fumée blanche, «&nbsp;360&nbsp;» dégradé Halo.")}</div>
  <div>{lbl("Indigo profond")}{tile(logo("logo-sq-neg", "38mm"), "indigo", "52mm", cap="Surfaces, cartes, ouvertures de section.")}</div>
  <div>{lbl("Noir")}{tile(logo("logo-sq-neg", "38mm"), "noir", "52mm", cap="Vidéo, événementiel, impression noir riche.")}</div>
  <div>{lbl("Photographie sombre")}{tile(logo("logo-sq-neg", "38mm"), "nuit", "52mm", style=photo_dark, cap="Zone calme et homogène, densité ≥ 70&nbsp;%.")}</div>
</div>
<div class="g g3" style="margin-top:8mm;gap:10mm">
  {blk("Contraste mesuré", txt("Fumée blanche sur Nuit spatiale&nbsp;: <b>17,38:1</b>. Halo cyan sur Nuit spatiale&nbsp;: <b>12,80:1</b>. Sur fond sombre, le cyan peut donc porter un titre ou un lien."))}
  {blk("Photographie", txt("Le logo se pose uniquement sur une zone calme et sombre de l'image. Si aucune zone ne convient, on change d'image — on n'ajoute ni bandeau ni cartouche derrière le logo."))}
  {blk("Interdit", txt("Contour, ombre portée ou lueur pour détacher le logo d'un fond trop clair&nbsp;: c'est le fond qu'on corrige, pas le logo."))}
</div>""")

# =================================================================== 12 fonds clairs
page("Fonds clairs", "Identité", f"""
<div class="g g4 gap-s">
  <div>{lbl("Blanc")}{tile(logo("logo-sq", "38mm"), "blanc", "52mm", cap="«&nbsp;Skill&nbsp;» Nuit, «&nbsp;360&nbsp;» dégradé Orbite.")}</div>
  <div>{lbl("Fumée blanche — référence")}{tile(logo("logo-sq", "38mm"), "fumee", "52mm", cap="Fond d'édition, papeterie, interfaces claires.")}</div>
  <div>{lbl("Bleu orbite")}{tile(logo("logo-sq-neg", "38mm", skill="#fff", n360="#fff"), "orbite", "52mm", cap="Uniquement la version monochrome blanche.")}</div>
  <div>{lbl("Photographie claire")}{tile(logo("logo-sq", "38mm"), "fumee", "52mm", style=photo_light, cap="Zone claire et homogène.")}</div>
</div>
<div class="g g3" style="margin-top:8mm;gap:10mm">
  {blk("Contraste mesuré", txt("Nuit spatiale sur Fumée blanche&nbsp;: <b>17,38:1</b>. Sur fond clair, le dégradé démarre en Cyan vif pour garder du relief&nbsp;; le cyan ne porte <b>jamais de texte</b> (1,96:1 sur blanc)."))}
  {blk("Fonds interdits", txt("Tout fond de clarté intermédiaire (gris moyens, bleus moyens, couleurs vives hors palette)&nbsp;: ni assez sombre pour la version négative, ni assez clair pour la version positive."))}
  {blk("Impression", txt("Sur papier non couché, le Nuit spatiale fonce et le dégradé s'éteint&nbsp;: prévoir une épreuve contractuelle pour tout tirage supérieur à 500 exemplaires."))}
</div>""")

# =================================================================== 13 interdictions
bad_grad = (f'<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="bad-g" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="0" x2="5026" y2="0"><stop offset="0" stop-color="{HALO}"/><stop offset="1" stop-color="{ORBITE}"/></linearGradient></defs></svg>')
o = DATA["orbit"]
x, y, w, h = DATA["viewbox_h"].split()
filled = (f'<svg class="L" viewBox="{DATA["viewbox_h"]}" style="width:44mm"><use href="#logotype" x="{x}" y="{y}" width="{w}" height="{h}" style="--lorb:transparent"/>'
          f'<circle cx="{fmt(o["cx"])}" cy="{fmt(o["cy"])}" r="{fmt(o["R"] - DATA["T"] / 2)}" fill="none" stroke="url(#logotype-orb)" stroke-width="{DATA["T"]}"/></svg>')
busy = ("background:conic-gradient(from 40deg at 30% 60%, #5A7BD8, #9FB4F0, #3E5FC4, #7FA0F2, #5A7BD8);")
bads = [
    (logo("logotype", "40mm", style="transform:scaleX(1.32)"), "blanc", "", "1. Déformer — toute homothétie non proportionnelle"),
    (logo("logotype", "40mm", style="transform:rotate(-14deg)"), "blanc", "", "2. Faire pivoter le logotype — seule l'Orbite tourne, et en mouvement"),
    (logo("logotype", "44mm", n360="#F2994A", skill="#5B2A86"), "blanc", "", "3. Recolorer hors palette"),
    (logo("logotype", "44mm", style="filter:drop-shadow(1.2mm 1.4mm .9mm rgba(0,0,0,.45))"), "blanc", "", "4. Ombre, contour, lueur, biseau ou relief"),
    (bad_grad + logo("logotype", "44mm", skill="url(#bad-g)"), "blanc", "", "5. Étendre le dégradé à «&nbsp;Skill&nbsp;»"),
    (filled, "blanc", "", "6. Combler les échappements ou remplacer l'Orbite par un zéro"),
    ('<span style="font:900 15pt/1 Arial Black, Arial;letter-spacing:-.02em;color:#070B1F">SKILL <span style="color:#2F6BFF">360</span></span>', "blanc", "", "7. Recomposer le logotype ou changer de police"),
    (logo("logotype", "44mm"), "fumee", busy, "8. Poser le logo sur un fond chargé ou de clarté moyenne"),
]
page("Interdictions", "Identité", f"""
<div class="g g4 gap-s">
  {"".join(tile(inner, bg, "32mm", style=st, cap=cap, extra='<span class="x-dot"></span>') for inner, bg, st, cap in bads)}
</div>
<div class="note" style="margin-top:6mm">La rotation appartient à l'Orbite, en mouvement uniquement (voir Motion, page 22). Sur un support fixe, le logotype ne tourne jamais, ne s'anime pas et ne se décompose pas.</div>""",
     lead="Ces huit cas couvrent l'essentiel des altérations constatées en pratique. Ils sont opposables.")

# =================================================================== 14 palette
main = COLORS["palette"][:5]
supp = COLORS["palette"][5:]
rows = []
for c in COLORS["palette"]:
    rows.append([f'<span class="sw" style="background:{c["hex"]}"></span>{c["name"]}', c["hex"],
                 " · ".join(str(v) for v in c["rgb"]), " · ".join(str(v) for v in c["cmyk"]), V if c["name"] in ("Nuit spatiale", "Bleu orbite", "Halo cyan", "Indigo profond", "Cyan vif") else "—", c["use"]])
sw = "".join(f'<div><div class="sw-big" style="background:{c["hex"]};{"border:.5pt solid var(--ligne)" if c["name"] == "Fumée blanche" else ""}"></div>'
             f'<p class="sw-n">{c["name"]}<small>{c["hex"]}</small></p></div>' for c in main)
sws = "".join(f'<div><div class="sw-big" style="height:12mm;background:{c["hex"]}"></div><p class="sw-n">{c["name"]}<small>{c["hex"]}</small></p></div>' for c in supp)
page("Palette", "Système", f"""
<div class="g" style="grid-template-columns:5fr 3fr;gap:8mm;margin-top:-3mm">
  <div>{lbl("Couleurs principales")}<div class="g g5 gap-s">{sw}</div></div>
  <div>{lbl("Tons d'appui")}<div class="g g3 gap-s">{sws}</div>
    <div class="g g2 gap-s" style="margin-top:3.4mm">
      <div><div class="sw-grad" style="background:linear-gradient(165deg,{CYAN},{ORBITE})"></div><p class="sw-n">Dégradé Orbite<small>fond clair</small></p></div>
      <div><div class="sw-grad" style="background:linear-gradient(165deg,{HALO},{ORBITE})"></div><p class="sw-n">Dégradé Halo<small>fond sombre</small></p></div>
    </div>
  </div>
</div>
<div style="margin-top:6mm">{tbl(rows, head=["Couleur", "HEX", "RVB", "CMJN indicatif", "Pantone", "Usage"], widths=["17%", "9%", "13%", "13%", "11%", "37%"])}</div>
<p class="cap" style="margin-top:2.4mm">CMJN&nbsp;: conversion indicative sans profil ICC, à arrêter sur épreuve avec l'imprimeur, comme les références Pantone. Écran&nbsp;: les boutons Bleu orbite utilisent la valeur interface <b>#2D69FC</b> (écart imperceptible) qui garantit 4,6:1 avec un libellé blanc.</p>""")

# =================================================================== 15 proportions & contrastes
pairs = [("Fumée blanche sur Nuit spatiale", FUMEE, NUIT), ("Halo cyan sur Nuit spatiale", HALO, NUIT),
         ("Brume sur Nuit spatiale", BRUME, NUIT), ("Fumée blanche sur Indigo profond", FUMEE, INDIGO),
         ("Blanc sur Bleu orbite interface #2D69FC", "#FFFFFF", "#2D69FC"), ("Blanc sur Bleu orbite #2F6BFF", "#FFFFFF", ORBITE),
         ("Bleu orbite sur Nuit spatiale", ORBITE, NUIT), ("Nuit spatiale sur Fumée blanche", NUIT, FUMEE),
         ("Ardoise sur Fumée blanche", ARDOISE, FUMEE), ("Bleu orbite sur Fumée blanche", ORBITE, FUMEE),
         ("Cyan vif sur blanc", CYAN, "#FFFFFF"), ("Halo cyan sur blanc", HALO, "#FFFFFF")]
crow = []
for label, fg, bg in pairs:
    r = contrast(fg, bg)
    crow.append([f'<span class="sw" style="background:{bg};color:{fg};font:800 5pt/4mm var(--t);text-align:center;width:6mm">Aa</span>{label}',
                 ratio_txt(r), wcag_level(r)])
legend = [("Nuit spatiale", NUIT, "50 %"), ("Fumée blanche", FUMEE, "30 %"), ("Indigo profond", INDIGO, "12 %"), ("Bleu orbite + Halo cyan", ORBITE, "8 %")]
bar = (f'<div style="display:flex;height:22mm;border-radius:1.6mm;overflow:hidden">'
       f'<div style="flex:50;background:{NUIT}"></div><div style="flex:30;background:{FUMEE};border-block:.5pt solid var(--ligne)"></div>'
       f'<div style="flex:12;background:{INDIGO}"></div><div style="flex:6;background:{ORBITE}"></div><div style="flex:2;background:{HALO}"></div></div>'
       f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.4mm 4mm;margin-top:2.4mm">'
       + "".join(f'<span style="display:flex;align-items:center;gap:1.8mm;font:600 6.2pt/1.2 var(--t)">'
                 f'<i style="width:2.6mm;height:2.6mm;border-radius:50%;background:{c};border:.4pt solid var(--ligne)"></i>{n}'
                 f'<b style="margin-left:auto;font:500 6pt/1 var(--d)">{p}</b></span>' for n, c, p in legend)
       + '</div>')
page("Proportions et contrastes", "Système", f"""
<div class="g" style="grid-template-columns:1fr 1.25fr;gap:12mm">
  <div>
    {lbl("Répartition type d'un support")}{bar}
    <div class="note" style="margin-top:6mm"><b>La règle des 8&nbsp;%.</b> La lumière est rare&nbsp;: Bleu orbite, Halo cyan et dégradés ne dépassent jamais 8&nbsp;% d'une surface. Au-delà, ils cessent de signaler et deviennent décor.</div>
    <div style="margin-top:6mm">{lbl("Ce que chaque couleur porte")}
    {tbl([["Nuit spatiale", "L'espace, la concentration, la rigueur."], ["Fumée blanche", "La respiration, la clarté, le texte."], ["Indigo profond", "La profondeur, les surfaces."], ["Bleu orbite", "L'action&nbsp;: boutons, liens, accents."], ["Halo cyan", "La lumière, le déclic, le «&nbsp;360&nbsp;»."]], widths=["32%", "68%"])}</div>
  </div>
  <div>{lbl("Contrastes mesurés — WCAG 2.1")}{tbl(crow, widths=["52%", "12%", "36%"])}
    <p class="cap" style="margin-top:2mm">Valeurs calculées sur les couleurs écran. Tout site, application ou document numérique doit atteindre le niveau AA.</p></div>
</div>""")

# =================================================================== 16 typographies
alpha = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
page("Typographies", "Système", f"""
<div class="g" style="grid-template-columns:1.12fr 1fr;gap:12mm;margin-top:-2mm">
  <div>
    {lbl("Titres et logotype — Unbounded")}
    <div style="display:flex;align-items:flex-end;gap:6mm"><span style="font:500 46pt/0.9 var(--d);letter-spacing:-.03em">Aa</span>
      <div><p class="mid" style="font-size:12pt">Unbounded</p><p class="sm mut">Light · Regular · <b>Medium</b> · SemiBold · ExtraBold (logotype)</p></div></div>
    <p style="font:400 8.2pt/1.45 var(--d);margin-top:3mm;letter-spacing:-.01em">{alpha[:26]}<br>{alpha[26:]}<br>0123456789 · àéèêçœ · «&nbsp;?&nbsp;!&nbsp;» · 360°</p>
    <p class="txt mut" style="margin-top:2mm">Une linéale étendue et géométrique, au dessin rond&nbsp;: elle porte le logotype, les titres, les chiffres clés et les accroches. Jamais pour le texte courant.</p>
    <div style="margin-top:6mm">{lbl("Texte — Manrope")}
    <div style="display:flex;align-items:flex-end;gap:6mm"><span style="font:600 46pt/0.9 var(--t);letter-spacing:-.02em">Aa</span>
      <div><p style="font:600 12pt/1.2 var(--t)">Manrope</p><p class="sm mut">Regular · Medium · SemiBold · <b>Bold</b> · ExtraBold</p></div></div>
    <p style="font:500 8.6pt/1.45 var(--t);margin-top:3mm">{alpha}<br>0123456789 · àéèêçœ · «&nbsp;?&nbsp;!&nbsp;» · 360°</p>
    <p class="txt mut" style="margin-top:2mm">Une linéale lisible et chaleureuse pour les programmes, les supports pédagogiques, les interfaces et le site.</p></div>
  </div>
  <div>
    {lbl("Hiérarchie")}
    {tbl([["Titre 1", "Unbounded Medium 32 pt / 1,05 — approche −2 %"], ["Titre 2", "Unbounded Medium 20 pt / 1,1"], ["Titre 3", "Manrope Bold 11 pt"],
          ["Surtitre", "Manrope Bold 7 pt — capitales, approche +24 %"], ["Chapô", "Manrope Regular 11 pt / 1,5"], ["Courant", "Manrope Regular 9 pt / 1,55"],
          ["Légende", "Manrope Medium 7 pt — Ardoise"], ["Chiffre clé", "Unbounded SemiBold 36 pt — dégradé"]], widths=["24%", "76%"])}
    <div style="margin-top:6mm">{blk("Substitutions bureautique", txt("Quand les polices ne peuvent pas être installées (Word, PowerPoint, e-mail)&nbsp;: titres en <b>Verdana</b> gras, texte en <b>Arial</b>. Jamais Calibri, jamais Comic Sans."))}</div>
    <p class="cap" style="margin-top:3mm">Unbounded et Manrope sont distribuées sous licence SIL Open Font License&nbsp;: usage commercial, web et intégration autorisés sans redevance. Fichiers fournis dans 04_Typographies.</p>
  </div>
</div>""")

# =================================================================== 17 grille
cols = "".join('<div style="background:#E6ECF8;border-radius:.6mm"></div>' for _ in range(12))
page("Grille", "Système", f"""
<div class="g" style="grid-template-columns:1.15fr 1fr;gap:12mm">
  <div>
    <div style="border:.5pt solid var(--ligne);border-radius:1.6mm;padding:5mm;height:70mm"><div style="display:grid;grid-template-columns:repeat(12,1fr);gap:2.4mm;height:100%">{cols}</div></div>
    <div class="g g2" style="margin-top:5mm;gap:8mm">
      {blk("Répartitions admises", txt("12 · 6 + 6 · 8 + 4 · 4 + 4 + 4 · 3 + 9 · 3 + 3 + 3 + 3."))}
      {blk("Pas de base", txt("<b>4 mm</b> à l'impression, <b>8 px</b> à l'écran. Tous les blocs s'y alignent."))}
    </div>
  </div>
  <div>
    {lbl("Réglages par format")}
    {tbl([["A4 paysage", "18 / 13 / 18 mm", "7 mm"], ["A4 portrait", "20 / 20 / 25 mm", "5 mm"], ["16:9", "6 % du côté", "1,5 %"], ["Web", "1 240 px utiles", "24 px"], ["Mobile", "20 px", "16 px · 4 col."]], head=["Format", "Marges", "Gouttière"], widths=["30%", "40%", "30%"])}
    <div style="margin-top:6mm">{blk("Principes", bul(["Le vide est l'espace de l'apprenant&nbsp;: on ne le remplit pas.", "Une seule idée dominante par page ou par écran.", "L'arc d'orbite ouvre un chapitre, nulle part ailleurs.", "Les textes s'alignent à gauche&nbsp;; on ne justifie jamais."]))}</div>
  </div>
</div>""", lead="Douze colonnes, un pas de base unique. La cohérence entre des supports très différents vient de là.")

# =================================================================== 18 photographie
ph = [("En situation", "Des apprenants en action, en atelier ou en classe virtuelle.", "linear-gradient(150deg,#1A2550,#070B1F)"),
      ("Le geste", "Le détail qui montre la compétence&nbsp;: des mains, un outil, un écran.", "linear-gradient(150deg,#2B3B6E,#0B1230)"),
      ("Portraits", "Formateurs et apprenants, regard franc, lumière douce.", "linear-gradient(150deg,#3A4A80,#121A44)"),
      ("Les lieux", "Salles, plateaux, espaces de pause&nbsp;: clairs et rangés.", "linear-gradient(150deg,#C9D3EA,#8C9BC4)")]
phs = "".join(f'<div><div class="tile" style="height:38mm;background:{bg};align-items:end;justify-items:start;padding:3mm">'
              + rings(820, 760, [260, 360, 470], style="position:absolute")
              + f'<span style="position:relative;font:700 4.8pt/1 var(--t);letter-spacing:.24em;text-transform:uppercase;color:#EEF2FA">{t}</span></div>'
              f'<p class="cap">{c}</p></div>' for t, c, bg in ph)
page("Photographie", "Système", f"""
<div class="g g4 gap-s">{phs}</div>
<div class="g g3" style="margin-top:7mm;gap:10mm">
  {blk("Traitement", bul(["Lumière naturelle, tons légèrement froids", "Profondeur de champ, un sujet net", "Formats 3:2 ou 16:9, sans cadre ni arrondi", "Diversité réelle des âges, des métiers, des profils"]))}
  {blk("Proscrit", bul(["Poignées de main, pouces levés, sourires figés", "Toques, tableaux noirs, pommes sur un bureau", "Images de banque génériques et personnes générées par IA", "Filtres, saturation forcée, vignettage"], "bul--x"))}
  {blk("Droits", txt(f"Autorisation écrite de chaque personne reconnaissable (droit à l'image) et cession de droits du photographe précisant supports, territoire et durée. Banque d'images à constituer par un reportage dans les salles et chez les clients&nbsp;{V}."))}
</div>""", lead="L'image porte la crédibilité de la formation. Une photographie générique la détruit plus vite qu'une absence d'image.")

# =================================================================== 19 données
bars = [34, 46, 41, 58, 66, 82]
bh = "".join(f'<div style="flex:1;height:{v}%;background:{NUIT if i < 5 else "linear-gradient(180deg," + CYAN + "," + ORBITE + ")"};border-radius:.6mm .6mm 0 0"></div>' for i, v in enumerate(bars))
line_svg = (f'<svg viewBox="0 0 300 120" style="width:100%;height:34mm;display:block">'
            f'<line x1="0" y1="118" x2="300" y2="118" stroke="#C9D0E2" stroke-width="1.2"/>'
            f'<polyline points="0,96 50,88 100,92 150,66 200,52 250,40 300,22" fill="none" stroke="{ORBITE}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<polyline points="0,104 50,100 100,98 150,92 200,88 250,84 300,78" fill="none" stroke="{BRUME}" stroke-width="2" stroke-dasharray="6 5"/>'
            f'<circle cx="300" cy="22" r="5" fill="{ORBITE}"/></svg>')
from logo_geom import orbit_segments
pr_segs, _ = orbit_segments(150, 150, 120, 92, (15, 135, 255), 10, 16)
prog = (f'<svg viewBox="0 0 300 300" style="width:34mm;height:34mm;display:block;margin:auto">'
        f'<defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{ORBITE}"/></linearGradient></defs>'
        f'<path d="{pr_segs[2]}" fill="url(#pg)"/><path d="{pr_segs[0]}" fill="url(#pg)"/><path d="{pr_segs[1]}" fill="#DCE3F3"/>'
        f'<text x="150" y="162" text-anchor="middle" font-family="Unbounded" font-weight="600" font-size="40" fill="{NUIT}">2/3</text></svg>')
page("Données et illustrations", "Système", f"""
<div class="g g3" style="gap:10mm">
  <div>{lbl("Histogramme")}<div style="display:flex;align-items:flex-end;gap:2.4mm;height:34mm;border-bottom:.6pt solid #C9D0E2">{bh}</div>
    <p class="cap">Barres Nuit, <b>dernière période en dégradé</b>. Ni contour, ni ombre, ni 3D.</p></div>
  <div>{lbl("Courbe")}{line_svg}<p class="cap">Série principale en Bleu orbite, référence en Brume pointillé.</p></div>
  <div>{lbl("Anneau de progression")}{prog}<p class="cap">Les trois segments de l'Orbite mesurent l'avancement d'un parcours.</p></div>
</div>
<div class="g g3" style="margin-top:7mm;gap:10mm">
  {blk("Règles", bul(["Axe des ordonnées démarrant à zéro, sans exception", "Unité, période et source sous chaque graphique", "Une seule couleur d'accent par graphique"]))}
  {blk("Proscrit", bul(["Camemberts multicolores, jauges, compteurs", "Axes tronqués qui exagèrent une progression", "Pictogrammes décoratifs dans les graphiques"], "bul--x"))}
  {blk("Motif de marque", txt("L'anneau de progression est le <b>seul graphique circulaire autorisé</b>&nbsp;: il reprend les trois segments de l'Orbite. Les données ci-dessus sont fictives, pour l'exemple."))}
</div>""", lead="Skill360 n'illustre pas&nbsp;: il montre. Partout où une donnée existe, le graphique remplace l'image d'ambiance.")

# =================================================================== 20 icônes
icons = [("management", "Management"), ("digital", "Digital"), ("ia", "Data & IA"), ("langues", "Langues"), ("commercial", "Commercial"), ("communication", "Communication"),
         ("rh", "RH & droit"), ("securite", "Prévention"), ("presentiel", "Présentiel"), ("visio", "Classe virtuelle"), ("mixte", "Mixte"), ("elearning", "E-learning"),
         ("cible", "Positionner"), ("parcours", "Construire"), ("livre", "Former"), ("certif", "Valoriser"), ("cpf", "Financement"), ("calendrier", "Sessions")]
ig = "".join(f'<figure>{icon(n, "7mm", NUIT)}<figcaption>{t}</figcaption></figure>' for n, t in icons)
page("Icônes", "Système", f"""
<div class="icons">{ig}</div>
<div class="g g3" style="margin-top:7mm;gap:10mm">
  {blk("Construction", tbl([["Grille", "24 × 24 px"], ["Zone utile", "20 × 20 px"], ["Épaisseur", "1,75 px constante"], ["Terminaisons", "arrondies, angles adoucis"]], widths=["40%", "60%"]))}
  {blk("Style", txt("Linéaire, monochrome, sans remplissage. Nuit spatiale ou Fumée blanche par défaut&nbsp;; <b>Halo cyan ou Bleu orbite pour l'état actif</b> d'une interface. Le jeu complet est fourni en SVG."))}
  {blk("Interdit", bul(["Mélanger deux jeux d'icônes", "Icônes pleines, duotones ou en dégradé", "Emoji sur un support institutionnel"], "bul--x"))}
</div>""", lead="Un jeu unique, dessiné pour la marque&nbsp;: domaines de formation, modalités, méthode et services.")

# =================================================================== 21 éléments graphiques
from logo_geom import circle_path
el_arcs = (f'<div class="tile tile--nuit" style="height:44mm">' + rings(500, 520, [180, 260, 350, 450], style="position:absolute", sats=[(260, 60, 7, HALO), (350, 210, 5, ORBITE)]) + '</div>')
el_halo = (f'<div class="tile tile--nuit" style="height:44mm"><div class="halo" style="width:46mm;height:46mm"></div>'
           f'<div class="halo halo--c" style="width:26mm;height:26mm"></div></div>')
el_point = (f'<div class="tile tile--nuit" style="height:44mm;gap:3mm;grid-auto-flow:column">'
            + "".join(f'<span style="width:{s}mm;height:{s}mm;border-radius:50%;background:linear-gradient(165deg,{HALO},{ORBITE})"></span>' for s in (3, 5, 8))
            + '</div>')
ch = orbit_segments(150, 150, 110, 70, (15, 135, 255), 12, 26)[0][2]
el_chev = (f'<div class="tile tile--nuit" style="height:44mm;gap:5mm;grid-auto-flow:column">'
           f'<svg viewBox="28 28 170 132" style="width:30mm;height:auto"><path d="{ch}" fill="{HALO}"/></svg>'
           f'<span style="font:700 6pt/1 var(--t);color:var(--fumee);letter-spacing:.1em;display:flex;align-items:center;gap:1.6mm">EN SAVOIR PLUS {icon("fleche", "4mm", HALO)}</span></div>')
page("Éléments graphiques", "Système", f"""
<div class="g g4 gap-s">
  <div>{lbl("L'arc d'orbite")}{el_arcs}<p class="cap">Filets de 0,5 à 1 pt, Fumée blanche à 10&nbsp;% sur fond sombre (Nuit à 8&nbsp;% sur fond clair). Satellites&nbsp;: points de 1 à 2 mm.</p></div>
  <div>{lbl("Le halo")}{el_halo}<p class="cap">Lumière diffuse Bleu orbite et Halo cyan, derrière le contenu. <b>Un seul halo par composition</b>, jamais sur le logo.</p></div>
  <div>{lbl("Le point")}{el_point}<p class="cap">Puce, repère, satellite. Toujours rond, toujours en dégradé Halo ou en Halo cyan plein.</p></div>
  <div>{lbl("Le segment")}{el_chev}<p class="cap">Un segment de l'Orbite, isolé, peut servir de signe de section. La flèche d'action reprend le trait des icônes.</p></div>
</div>
<div class="note" style="margin-top:7mm">Les éléments graphiques s'additionnent avec parcimonie&nbsp;: <b>au plus deux par composition</b> (par exemple un arc d'orbite et un halo). Ils ne recouvrent jamais un texte et ne s'approchent pas du logo à moins de sa zone de protection.</div>""",
     lead="Quatre éléments dérivés de l'Orbite et du concept de marque. Ils structurent les compositions sans jamais concurrencer le logo.")

# =================================================================== 22 motion
frames = [("0,0 s", "Le point", "L'apprenant apparaît, un halo s'allume."),
          ("0,5 s", "L'orbite se trace", "Un trait de lumière fait le tour du point."),
          ("1,3 s", "Rotation et morphing", "Le O fait un tour complet en se gonflant, puis se fend en trois segments."),
          ("2,3 s", "Verrouillage", "Les segments se resserrent avec un léger rebond élastique."),
          ("2,8 s", "Écriture", "Le O roule à sa place, le point rejoint le i, le logotype se trace puis se remplit."),
          ("4,0 s", "Signature", "La signature apparaît lettre à lettre, l'Orbite se verrouille, le halo s'éteint.")]
mf = "".join(f'<figure><img src="img/motion-{i + 1}.jpg"><figcaption><b><i>{a}</i>{b}</b>{c}</figcaption></figure>' for i, (a, b, c) in enumerate(frames))
page("Motion — l'animation du logo", "Système", f"""
<div class="g" style="grid-template-columns:1.85fr 1fr;gap:9mm;margin-top:-3mm">
  <div class="motion" style="grid-template-columns:1fr 1fr;gap:3mm 4mm">{mf}</div>
  <div>
    {lbl("Réglages")}
    {tbl([["Durée", "5,7 s, une seule lecture"], ["Rotation", "sens horaire, par tours complets (360°, 720°)"], ["Courbes", "power3.inOut (rotation), elastic.out (morphing), power2.inOut (écriture)"],
          ["Outils", "GSAP 3 — MorphSVG, DrawSVG, ScrollTrigger"], ["Accessibilité", "«&nbsp;Réduire les animations&nbsp;» activé&nbsp;: logo affiché directement dans son état final"]], widths=["30%", "70%"])}
    <div style="margin-top:5mm">{blk("Principes", bul(["Seule l'Orbite tourne&nbsp;; le lettrage s'écrit, il ne bouge pas.", "Le halo n'existe qu'en mouvement.", "Une animation du logo par écran, au chargement ou à la demande.", "Fichier de référence&nbsp;: 07_Site_Web/animation-logo.html."]))}</div>
  </div>
</div>""", lead="Le logo s'écrit après une rotation de l'Orbite. C'est la seule animation de marque&nbsp;: elle ouvre le site, les vidéos et les présentations.")
