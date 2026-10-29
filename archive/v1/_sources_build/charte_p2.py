"""Charte Skill360 — partie II : applications et annexes."""
from charte_lib import *
from logo_geom import orbit_segments, fmt

NUIT, INDIGO, ORBITE, HALO, FUMEE, CYAN = C["nuit"], C["indigo"], C["orbite"], C["halo"], C["fumee"], C["cyan"]
ARDOISE, BRUME = "#4A5170", "#A6AFCC"
GPOS = f"linear-gradient(165deg,{CYAN},{ORBITE})"
GNEG = f"linear-gradient(165deg,{HALO},{ORBITE})"


def lines(n, widths=None, gap=None, color=None):
    out = []
    for i in range(n):
        w = (widths or [100, 92, 96, 70])[i % len(widths or [100, 92, 96, 70])]
        st = f"width:{w}%;" + (f"margin-top:{gap};" if gap else "") + (f"background:{color};" if color else "")
        out.append(f'<div class="mk-line" style="{st}"></div>')
    return "".join(out)


def k(t, size="4pt", color=ARDOISE, weight=700, ls=".2em", extra=""):
    return f'<p style="font:{weight} {size}/1.3 var(--t);letter-spacing:{ls};text-transform:uppercase;color:{color};{extra}">{t}</p>'


# =================================================================== mockups (re-used on the overview page)
def card_recto(w=85, h=55):
    return (f'<div class="mk mk-dark shadow" style="width:{w}mm;height:{h}mm;border-radius:1mm;display:grid;place-items:center">'
            + rings(760, 520, [300, 400, 520], style="position:absolute", sats=[(400, 300, 8, HALO)])
            + f'{logo("logo-h-neg", f"{w * .62:.1f}mm", style="position:relative")}</div>')


def card_verso(w=85, h=55):
    s = w / 85
    return (f'<div class="mk mk-fumee shadow" style="width:{w}mm;height:{h}mm;border-radius:1mm;padding:{7 * s:.1f}mm {7 * s:.1f}mm">'
            f'<p style="font:500 {9 * s:.1f}pt/1.1 var(--d);letter-spacing:-.01em">Prénom Nom</p>'
            f'{k("Fonction " + V, f"{4.6 * s:.1f}pt", ORBITE, extra="margin-top:1.4mm")}'
            f'<span style="display:block;width:{8 * s:.1f}mm;height:.8pt;background:{GPOS};margin:{3.2 * s:.1f}mm 0"></span>'
            f'<p style="font:500 {5.6 * s:.1f}pt/1.75 var(--t);color:{NUIT}">T. {V}<br>prenom.nom@skill360.fr<br><b>skill360.fr</b></p>'
            f'<div style="position:absolute;right:{6 * s:.1f}mm;bottom:{6 * s:.1f}mm">{logo("orbite", f"{9 * s:.1f}mm")}</div>'
            f'<p style="position:absolute;left:{7 * s:.1f}mm;bottom:{6.4 * s:.1f}mm;font:600 {4.2 * s:.1f}pt/1 var(--t);letter-spacing:.18em;text-transform:uppercase;color:{ARDOISE}">Développer ses compétences à 360°</p></div>')


def slide(kind, w=80):
    h = w * 9 / 16
    s = w / 80
    base = f'class="mk shadow" style="width:{w}mm;height:{h:.1f}mm;border-radius:.8mm;'
    if kind == "cover":
        return (f'<div {base}background:{NUIT};color:{FUMEE};padding:{6 * s:.1f}mm">'
                + rings(860, 640, [260, 360, 470], style="position:absolute", sats=[(360, 290, 9, HALO)])
                + f'{logo("logotype-neg", f"{24 * s:.1f}mm", style="position:relative")}'
                f'<p style="position:absolute;left:{6 * s:.1f}mm;bottom:{9 * s:.1f}mm;font:400 {9 * s:.1f}pt/1.1 var(--d);letter-spacing:-.02em">Titre de la<br>présentation</p>'
                f'<p style="position:absolute;left:{6 * s:.1f}mm;bottom:{5 * s:.1f}mm;font:700 {3.4 * s:.1f}pt/1 var(--t);letter-spacing:.2em;color:{BRUME}">SESSION · DATE</p></div>')
    if kind == "section":
        return (f'<div {base}background:{FUMEE};padding:{7 * s:.1f}mm">'
                f'<p style="font:600 {20 * s:.1f}pt/1 var(--d);background:{GPOS};-webkit-background-clip:text;background-clip:text;color:transparent">01</p>'
                f'<p style="margin-top:{3 * s:.1f}mm;font:400 {9 * s:.1f}pt/1.15 var(--d);letter-spacing:-.02em">Positionner<br>avant de former</p>'
                f'<div style="position:absolute;right:{5 * s:.1f}mm;bottom:{4 * s:.1f}mm">{logo("orbite", f"{5 * s:.1f}mm")}</div></div>')
    if kind == "text":
        return (f'<div {base}background:#fff;padding:{6 * s:.1f}mm;display:grid;grid-template-columns:1fr 1fr;gap:{5 * s:.1f}mm">'
                f'<div><p style="font:400 {6.5 * s:.1f}pt/1.15 var(--d)">Titre de la diapositive</p><div style="margin-top:{4 * s:.1f}mm">{lines(5)}</div></div>'
                f'<div style="border-radius:.8mm;background:linear-gradient(150deg,#2B3B6E,#0B1230)"></div></div>')
    if kind == "data":
        bars = "".join(f'<div style="flex:1;height:{v}%;background:{NUIT if i < 4 else GPOS};border-radius:.4mm .4mm 0 0"></div>' for i, v in enumerate([30, 44, 40, 58, 80]))
        return (f'<div {base}background:#fff;padding:{6 * s:.1f}mm">'
                f'<p style="font:400 {6.5 * s:.1f}pt/1.15 var(--d)">Taux de réalisation</p>'
                f'<div style="display:flex;align-items:flex-end;gap:{2.2 * s:.1f}mm;height:{24 * s:.1f}mm;margin-top:{3 * s:.1f}mm;border-bottom:.5pt solid #C9D0E2">{bars}</div>'
                f'<p style="margin-top:1mm;font:500 {3 * s:.1f}pt/1 var(--t);color:{ARDOISE}">Données fictives — source, période</p></div>')
    if kind == "quote":
        return (f'<div {base}background:{NUIT};color:{FUMEE};padding:{7 * s:.1f}mm">'
                f'<p style="font:300 {7.4 * s:.1f}pt/1.3 var(--d);letter-spacing:-.01em">«&nbsp;On entre dans l\'orbite, on en ressort <span class="grad-neg">grandi</span>.&nbsp;»</p>'
                f'<div style="position:absolute;left:{7 * s:.1f}mm;bottom:{5 * s:.1f}mm">{logo("orbite-neg", f"{5 * s:.1f}mm")}</div></div>')


def phone(inner, w=40, h=82):
    return f'<div class="phone shadow" style="width:{w}mm;height:{h}mm"><div class="phone__screen">{inner}</div></div>'


def prog_ring(size, frac, dark=True):
    segs, _ = orbit_segments(50, 50, 46, 34, (15, 135, 255), 5, 7)
    order = [2, 0, 1]
    filled = round(frac * 3)
    p = "".join(f'<path d="{segs[s]}" fill="{"url(#rg)" if i < filled else ("rgba(238,242,250,.15)" if dark else "#DCE3F3")}"/>' for i, s in enumerate(order))
    return (f'<svg viewBox="0 0 100 100" style="width:{size};height:{size};flex:none"><defs><linearGradient id="rg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{HALO}"/><stop offset="1" stop-color="{ORBITE}"/></linearGradient></defs>{p}</svg>')


def app_launch():
    return (f'<div style="height:100%;background:radial-gradient(80% 60% at 50% 42%,#14205A,{NUIT} 70%);display:grid;place-items:center;position:relative">'
            + rings(500, 430, [230, 320, 420], style="position:absolute")
            + f'<div style="display:grid;justify-items:center;gap:3mm;position:relative">{logo("orbite-neg", "15mm")}{logo("logotype-neg", "20mm")}</div></div>')


def app_list():
    items = [("Prendre la parole en public", 1), ("Excel&nbsp;: tableaux croisés", 2 / 3), ("Manager à distance", 1 / 3)]
    rows = "".join(f'<div style="display:flex;gap:2mm;align-items:center;padding:2.2mm 0;border-bottom:.4pt solid rgba(238,242,250,.12)">'
                   f'{prog_ring("6.5mm", f)}<div><p style="font:700 4.1pt/1.25 var(--t);color:{FUMEE}">{t}</p>'
                   f'<p style="font:500 3.4pt/1.3 var(--t);color:{BRUME}">{round(f * 3)}/3 dimensions</p></div></div>' for t, f in items)
    return (f'<div style="height:100%;background:{NUIT};padding:7mm 3.5mm 3mm;color:{FUMEE}">'
            f'{k("Mes parcours", "3.4pt", HALO)}<p style="font:500 6.4pt/1.15 var(--d);margin:1.4mm 0 2mm">Bonjour Camille</p>{rows}'
            f'<div style="margin-top:3mm;border-radius:1.4mm;background:{INDIGO};padding:2.4mm"><p style="font:700 3.6pt/1.3 var(--t)">Prochaine session</p>'
            f'<p style="font:500 3.3pt/1.3 var(--t);color:{BRUME}">Classe virtuelle · jeudi 9&nbsp;h</p></div></div>')


def app_module():
    return (f'<div style="height:100%;background:{FUMEE};color:{NUIT}">'
            f'<div style="height:28mm;background:linear-gradient(150deg,#2B3B6E,#0B1230);display:grid;place-items:center">'
            f'<span style="width:7mm;height:7mm;border-radius:50%;background:{ORBITE};display:grid;place-items:center">'
            f'<span style="width:0;height:0;border-left:2mm solid #fff;border-top:1.3mm solid transparent;border-bottom:1.3mm solid transparent;margin-left:.6mm"></span></span></div>'
            f'<div style="padding:3mm 3.5mm">{k("Module 2 · Savoir-faire", "3.3pt", ORBITE)}'
            f'<p style="font:500 5.6pt/1.2 var(--d);margin-top:1.2mm">Structurer son message</p>'
            f'<div style="margin-top:2mm;height:1.2mm;border-radius:1mm;background:#DCE3F3"><div style="width:62%;height:100%;border-radius:1mm;background:{GPOS}"></div></div>'
            f'<div style="margin-top:2.4mm">{lines(4)}</div>'
            f'<div style="margin-top:3mm;height:6mm;border-radius:3mm;background:{C["nuit"]};color:#fff;display:grid;place-items:center;font:700 3.6pt/1 var(--t)">Continuer</div></div></div>')


def kakemono(w=34):
    h = w * 200 / 85
    s = w / 34
    return (f'<div class="mk mk-dark shadow" style="width:{w}mm;height:{h:.1f}mm;border-radius:.6mm;padding:{4 * s:.1f}mm {3.4 * s:.1f}mm">'
            + f'{logo("logo-h-neg", f"{27 * s:.1f}mm")}'
            f'<p style="margin-top:{9 * s:.1f}mm;font:400 {7.6 * s:.1f}pt/1.12 var(--d);letter-spacing:-.02em">Développer ses compétences <span class="grad-neg">à&nbsp;360°</span>.</p>'
            f'<div style="position:absolute;left:{-8 * s:.1f}mm;bottom:{-10 * s:.1f}mm;opacity:.95">{logo("orbite-neg", f"{50 * s:.1f}mm")}</div>'
            f'<p style="position:absolute;right:{3.4 * s:.1f}mm;bottom:{3 * s:.1f}mm;font:700 {3.2 * s:.1f}pt/1 var(--t);letter-spacing:.18em;color:{FUMEE}">SKILL360.FR</p></div>')


def tote(w=46):
    s = w / 46
    return (f'<div style="position:relative;width:{w}mm;height:{58 * s:.1f}mm">'
            f'<div style="position:absolute;left:{12 * s:.1f}mm;top:0;width:{22 * s:.1f}mm;height:{20 * s:.1f}mm;border:{1.6 * s:.1f}mm solid #1B2140;border-bottom:none;border-radius:{11 * s:.1f}mm {11 * s:.1f}mm 0 0"></div>'
            f'<div class="shadow" style="position:absolute;left:0;right:0;top:{12 * s:.1f}mm;bottom:0;background:{NUIT};border-radius:.6mm;display:grid;place-items:center">'
            f'<div style="display:grid;justify-items:center;gap:{3 * s:.1f}mm">{logo("orbite-neg", f"{20 * s:.1f}mm", n360=HALO)}{logo("logotype-neg", f"{22 * s:.1f}mm", n360=HALO)}</div></div></div>')


def social_post(kind, w=40):
    s = w / 40
    if kind == "dark":
        return (f'<div class="mk mk-dark shadow" style="width:{w}mm;height:{w}mm;border-radius:.6mm;padding:{4 * s:.1f}mm">'
                + rings(820, 820, [300, 420], style="position:absolute")
                + f'{k("Nouvelle session", f"{3.2 * s:.1f}pt", HALO)}'
                f'<p style="margin-top:{2 * s:.1f}mm;font:400 {7 * s:.1f}pt/1.12 var(--d);letter-spacing:-.02em">Manager<br>une équipe<br>à distance</p>'
                f'<p style="margin-top:{2 * s:.1f}mm;font:600 {3.6 * s:.1f}pt/1.3 var(--t);color:{BRUME}">2 jours · classe virtuelle</p>'
                f'<div style="position:absolute;right:{4 * s:.1f}mm;bottom:{4 * s:.1f}mm">{logo("orbite-neg", f"{6 * s:.1f}mm")}</div></div>')
    if kind == "light":
        return (f'<div class="mk mk-fumee shadow" style="width:{w}mm;height:{w}mm;border-radius:.6mm;padding:{4 * s:.1f}mm">'
                f'{k("Conseil", f"{3.2 * s:.1f}pt", ORBITE)}'
                f'<p style="margin-top:{2 * s:.1f}mm;font:400 {6.4 * s:.1f}pt/1.15 var(--d);letter-spacing:-.02em">3 réflexes pour prendre la parole sans stress</p>'
                f'<div style="position:absolute;left:{4 * s:.1f}mm;bottom:{4 * s:.1f}mm">{logo("logotype", f"{14 * s:.1f}mm")}</div></div>')
    return (f'<div class="mk shadow" style="width:{w}mm;height:{w}mm;border-radius:.6mm;padding:{4 * s:.1f}mm;background:{INDIGO};color:{FUMEE}">'
            f'{k("Parcours", f"{3.2 * s:.1f}pt", HALO)}'
            f'<p style="margin-top:{2 * s:.1f}mm;font:300 {5.6 * s:.1f}pt/1.3 var(--d)">«&nbsp;J\'ai repris confiance en trois semaines.&nbsp;»</p>'
            f'<p style="margin-top:{1.6 * s:.1f}mm;font:600 {3.4 * s:.1f}pt/1.3 var(--t);color:{BRUME}">Prénom, apprenante — avec son accord</p>'
            f'<div style="position:absolute;right:{4 * s:.1f}mm;bottom:{4 * s:.1f}mm">{logo("orbite-neg", f"{6 * s:.1f}mm")}</div></div>')


def plaque(w=80):
    s = w / 80
    return (f'<div class="mk mk-fumee shadow" style="width:{w}mm;height:{w * .62:.1f}mm;border-radius:.8mm;padding:{6 * s:.1f}mm">'
            f'{icon("management", f"{7 * s:.1f}mm", ORBITE)}'
            f'<p style="margin-top:{4 * s:.1f}mm;font:400 {10 * s:.1f}pt/1.05 var(--d);letter-spacing:-.02em">Salle<br>Exploration</p>'
            f'{k("Niveau 1 · 14 places", f"{3.6 * s:.1f}pt", ARDOISE, extra=f"margin-top:{3 * s:.1f}mm")}'
            f'<div style="position:absolute;right:{6 * s:.1f}mm;bottom:{6 * s:.1f}mm">{logo("orbite", f"{8 * s:.1f}mm")}</div></div>')


def certificate(w=142):
    s = w / 142
    h = w * 210 / 297
    return (f'<div class="mk mk-fumee shadow" style="width:{w}mm;height:{h:.1f}mm;border-radius:.6mm;padding:{9 * s:.1f}mm {11 * s:.1f}mm">'
            f'<div style="position:absolute;right:{-20 * s:.1f}mm;top:{-6 * s:.1f}mm;opacity:.06">{logo("orbite", f"{95 * s:.1f}mm", n360=NUIT)}</div>'
            f'{logo("logo-h", f"{44 * s:.1f}mm", style="position:relative")}'
            f'<p style="position:relative;margin-top:{9 * s:.1f}mm;font:400 {13 * s:.1f}pt/1.05 var(--d);letter-spacing:-.025em">Attestation de<br>fin de formation</p>'
            f'<span style="display:block;width:{12 * s:.1f}mm;height:1.1pt;background:{GPOS};margin:{4 * s:.1f}mm 0"></span>'
            f'<p style="position:relative;font:500 {5.6 * s:.1f}pt/1.6 var(--t);color:{ARDOISE}">délivrée à</p>'
            f'<p style="position:relative;font:500 {10 * s:.1f}pt/1.2 var(--d);letter-spacing:-.01em">Prénom Nom</p>'
            f'<p style="position:relative;margin-top:{2.6 * s:.1f}mm;font:500 {5.6 * s:.1f}pt/1.65 var(--t);color:{NUIT}">pour avoir suivi la formation <b>«&nbsp;Prendre la parole en public&nbsp;»</b><br>'
            f'du [date] au [date] — durée&nbsp;: 14 heures — modalité&nbsp;: présentiel<br>Évaluation des acquis&nbsp;: objectifs atteints</p>'
            f'<div style="position:absolute;left:{11 * s:.1f}mm;right:{11 * s:.1f}mm;bottom:{8 * s:.1f}mm;display:flex;justify-content:space-between;align-items:flex-end;font:600 {4.4 * s:.1f}pt/1.5 var(--t);color:{ARDOISE}">'
            f'<span>Fait à [ville], le [date]</span><span style="border-top:.5pt solid {NUIT};padding-top:1mm;width:{40 * s:.1f}mm;text-align:center">Responsable pédagogique</span></div></div>')


def facade(w=250, h=82):
    return (f'<div class="mk shadow" style="width:{w}mm;height:{h}mm;border-radius:1mm;background:linear-gradient(180deg,#2A3047,#151A2C 70%,#0C0F1C)">'
            f'<div style="position:absolute;left:0;right:0;bottom:0;height:16mm;background:repeating-linear-gradient(90deg,#1C2236 0 20mm,#232A42 20mm 21mm)"></div>'
            f'<div style="position:absolute;left:28mm;right:28mm;top:13mm;height:40mm;background:#0A0E1E;border-radius:.6mm;display:grid;place-items:center">'
            f'<div style="filter:drop-shadow(0 0 2.4mm rgba(111,224,255,.35))">{logo("logotype-neg", "140mm", n360=HALO)}</div></div></div>')


def browser(img, w):
    return (f'<div class="browser shadow" style="width:{w}"><div class="browser__bar"><i></i><i></i><i></i><b>skill360.fr</b></div>'
            f'<img src="{img}"></div>')


# =================================================================== 23 cartes de visite
page("Cartes de visite", "Papeterie", f"""
<div class="g" style="grid-template-columns:85mm 85mm 1fr;gap:9mm;margin-top:2mm">
  <div>{lbl("Recto")}{card_recto()}</div>
  <div>{lbl("Verso")}{card_verso()}</div>
  <div>
    {lbl("Fabrication")}
    {tbl([["Format", "85 × 55 mm, angles droits"], ["Support", "400 g/m², couché mat"], ["Recto", "aplat Nuit spatiale, pelliculage soft touch"], ["Dégradé", "quadrichromie, sans vernis sélectif"], ["Verso", "Fumée blanche, texte Nuit spatiale"], ["Coupe", "franche, fond perdu 3 mm"]], widths=["32%", "68%"])}
    <p class="cap" style="margin-top:3mm">Une seule mise en page. Seuls le nom, la fonction et les coordonnées changent. Le logotype n'est jamais réduit sous 50 mm au recto.</p>
  </div>
</div>
<div class="g g3" style="margin-top:9mm;gap:10mm">
  {blk("Nom", txt("Unbounded Medium 9 pt, Nuit spatiale. Prénom et nom en minuscules accentuées, jamais en capitales."))}
  {blk("Fonction", txt("Manrope Bold 4,6 pt, capitales, approche +20 %, Bleu orbite."))}
  {blk("Coordonnées", txt("Manrope Medium 5,6 pt / 1,75. Téléphone, e-mail, site — dans cet ordre, sans pictogrammes."))}
</div>""")

# =================================================================== 24 papier à en-tête
sheet1 = (f'<div class="mk mk-white shadow" style="width:76mm;height:107.5mm;padding:7.2mm 7.2mm">'
          f'{logo("logo-h", "17mm")}'
          f'<div style="margin:9mm 0 0 38mm">{lines(4, [100, 80, 90, 60])}</div>'
          f'<p style="margin-top:7mm;font:500 3.3pt/1 var(--t);color:{ARDOISE}">[Ville], le [date]</p>'
          f'<div style="margin-top:5mm">{lines(13, [100, 96, 98, 90, 100, 94, 60])}</div>'
          f'<div style="position:absolute;left:7.2mm;right:7.2mm;bottom:5.6mm;border-top:.4pt solid #D6DCEA;padding-top:1.2mm;font:500 2.3pt/1.5 var(--t);color:{ARDOISE}">'
          f'Skill360 — [forme juridique] au capital de [—] — [adresse] — SIRET [—] — Déclaration d\'activité n° [—] (cet enregistrement ne vaut pas agrément de l\'État) — skill360.fr</div></div>')
sheet2 = (f'<div class="mk mk-white shadow" style="width:76mm;height:107.5mm;padding:7.2mm 7.2mm">'
          f'{logo("orbite", "5mm")}<div style="margin-top:9mm">{lines(16, [100, 96, 98, 90, 100, 94, 72])}</div>'
          f'<p style="position:absolute;right:7.2mm;bottom:5.6mm;font:500 3pt/1 var(--d);color:{NUIT}">2</p></div>')
page("Papier à en-tête", "Papeterie", f"""
<div class="g" style="grid-template-columns:76mm 76mm 1fr;gap:9mm;margin-top:-3mm">
  <div>{lbl("Premier feuillet")}{sheet1}</div>
  <div>{lbl("Feuillets suivants")}{sheet2}</div>
  <div>
    {lbl("Réglages")}
    {tbl([["Format", "A4 — 210 × 297 mm"], ["Support", "100 g/m², offset blanc"], ["Marges", "20 / 20 / 25 mm"], ["Logo", "principal, 45 mm, en haut à gauche"], ["Texte", "Manrope Regular 10 / 15 pt"], ["Pied", "Manrope Medium 6,5 pt, Ardoise"]], widths=["30%", "70%"])}
    <div style="margin-top:6mm">{blk("Mentions légales", txt(f"Dénomination, forme juridique, capital, siège, SIRET, numéro de déclaration d'activité et mention «&nbsp;Cet enregistrement ne vaut pas agrément de l'État&nbsp;» figurent en pied de tout courrier. Valeurs {V}&nbsp;: elles se reprennent des statuts."))}</div>
    <p class="cap" style="margin-top:3mm">Le modèle Word reprend exactement ce gabarit (voir page 28). Les feuillets suivants ne portent que l'Orbite.</p>
  </div>
</div>""")

# =================================================================== 25 enveloppes
dl = (f'<div class="mk mk-white shadow" style="width:120mm;height:60mm;padding:6mm 7mm">{logo("logo-h", "36mm")}'
      f'<div style="position:absolute;left:10mm;top:26mm;width:52mm;height:24mm;border:.6pt dashed #AEB8D2;border-radius:1mm;padding:1.6mm 2mm;font:700 3pt/1 var(--t);letter-spacing:.2em;color:{ARDOISE}">FENÊTRE — DESTINATAIRE</div></div>')
c5 = (f'<div class="mk mk-dark shadow" style="width:100mm;height:70.7mm;padding:7mm">'
      + rings(820, 760, [260, 360, 470], style="position:absolute", sats=[(360, 300, 8, HALO)])
      + f'<div style="position:relative">{logo("orbite-neg", "11mm")}</div>'
      f'<p style="position:absolute;left:7mm;bottom:6mm;font:700 3.4pt/1 var(--t);letter-spacing:.24em;color:{BRUME}">SKILL360 · FORMATION &amp; DÉVELOPPEMENT DES COMPÉTENCES</p></div>')
page("Enveloppes", "Papeterie", f"""
<div class="g" style="grid-template-columns:120mm 100mm;gap:12mm;align-items:start">
  <div>{lbl("DL 110 × 220 — à fenêtre")}{dl}</div>
  <div>{lbl("C5 — envois de prestige")}{c5}</div>
</div>
<div class="g g3" style="margin-top:9mm;gap:10mm">
  {blk("Usage", txt("L'enveloppe blanche couvre le courrier courant. L'enveloppe Nuit spatiale est réservée aux envois remarquables&nbsp;: attestations, conventions, catalogues, invitations."))}
  {blk("Règles", bul(["Logo en haut à gauche, 36 mm", "Zone d'affranchissement laissée libre", "Patte de fermeture nue ou Orbite seule"]))}
  {blk("À confirmer", txt(f"Cotes de fenêtre et zones réservées auprès de l'opérateur postal {V}."))}
</div>""")

# =================================================================== 26 signature e-mail
sig = (f'<div class="tile tile--blanc" style="display:block;place-items:normal;padding:8mm 9mm;height:auto">'
       f'<p style="font:400 7.2pt/1.4 Arial;color:{NUIT}">Bien cordialement,</p>'
       f'<div style="display:flex;gap:5mm;margin-top:5mm;align-items:flex-start">'
       f'<div style="width:15mm;height:15mm;border-radius:1.4mm;background:{NUIT};display:grid;place-items:center;flex:none">{logo("orbite-neg", "9.5mm")}</div>'
       f'<div style="border-left:.6pt solid #D6DCEA;padding-left:5mm">'
       f'<p style="font:700 8pt/1.3 Arial;color:{NUIT}">Prénom Nom</p>'
       f'<p style="font:700 5.4pt/1.4 Arial;letter-spacing:.12em;color:{ORBITE}">FONCTION {V} · SKILL360</p>'
       f'<span style="display:block;width:9mm;height:.8pt;background:{GPOS};margin:2.4mm 0"></span>'
       f'<p style="font:400 6.4pt/1.7 Arial;color:{NUIT}">T. {V}<br>prenom.nom@skill360.fr<br><b>skill360.fr</b></p>'
       f'<p style="margin-top:2mm;font:400 5.6pt/1.4 Arial;color:{ARDOISE}">Développer ses compétences à 360°.</p></div></div></div>')
page("Signature e-mail", "Digital", f"""
<div class="g" style="grid-template-columns:1.15fr 1fr;gap:12mm">
  <div>{lbl("Rendu")}{sig}</div>
  <div>
    {blk("Contraintes techniques", bul(["Tableau HTML, styles en ligne, aucune feuille externe", "Orbite sur carré Nuit, PNG 120 px (affiché 60 px), attribut alt renseigné", "Texte en Arial&nbsp;: les polices de marque ne se chargent pas dans les messageries", "Largeur maximale 480 px, poids total inférieur à 40 Ko"]))}
    {blk("Proscrit", bul(["Bannières animées, citations, slogans de campagne", "Icônes de réseaux sociaux en couleurs", "Signature entièrement en image"], "bul--x"))}
    <p class="cap" style="margin-top:4mm">Déploiement centralisé depuis la messagerie de l'entreprise. Mention de confidentialité à arrêter avec le conseil juridique {V}.</p>
  </div>
</div>""")

# =================================================================== 27 présentation
page("Présentation", "Bureautique", f"""
<div class="g g3 gap-s" style="justify-items:start">
  <div>{slide("cover")}<p class="cap">1 — Couverture</p></div>
  <div>{slide("section")}<p class="cap">2 — Ouverture de section</p></div>
  <div>{slide("text")}<p class="cap">3 — Texte et visuel</p></div>
  <div>{slide("data")}<p class="cap">4 — Données</p></div>
  <div>{slide("quote")}<p class="cap">5 — Citation</p></div>
  <div>{lbl("Réglages")}{tbl([["Format", "16:9 — 33,87 × 19,05 cm"], ["Titres", "Unbounded Regular 28 pt"], ["Texte", "Manrope Regular 14 pt"], ["Pied", "Orbite 6 mm + numéro"]], widths=["32%", "68%"])}
    <p class="cap" style="margin-top:2mm">Pas de transition décorative. Masques verrouillés dans le modèle.</p></div>
</div>""", lead="Un gabarit unique en 16:9, cinq dispositions. Aucune diapositive ne se compose en dehors.")

# =================================================================== 28 documents bureautiques
doc = (f'<div class="mk mk-white shadow" style="width:88mm;height:124.5mm;padding:9mm 9mm">{logo("logo-h", "22mm")}'
       f'<p style="margin-top:12mm;font:400 9pt/1.15 var(--d);letter-spacing:-.02em">Titre du document</p>'
       f'<span style="display:block;width:8mm;height:.9pt;background:{GPOS};margin:3mm 0"></span>'
       f'{k("Titre de niveau 2", "3.4pt", ARDOISE)}<div style="margin-top:2mm">{lines(8)}</div>'
       f'{k("Titre de niveau 2", "3.4pt", ARDOISE, extra="margin-top:4mm")}<div style="margin-top:2mm">{lines(6)}</div>'
       f'<div style="margin-top:4mm;border-top:.6pt solid {NUIT}">' + "".join(f'<div style="display:flex;gap:3mm;padding:1.1mm 0;border-bottom:.4pt solid #E0E5F0">{lines(1, [40])}{lines(1, [30])}</div>' for _ in range(3)) + '</div>'
       f'<p style="position:absolute;left:9mm;bottom:6mm;font:500 2.6pt/1 var(--t);color:{ARDOISE}">Skill360</p>'
       f'<p style="position:absolute;right:9mm;bottom:6mm;font:500 2.8pt/1 var(--d)">1</p></div>')
page("Documents bureautiques", "Bureautique", f"""
<div class="g" style="grid-template-columns:88mm 1fr;gap:12mm;margin-top:-3mm">
  <div>{lbl("Document courant")}{doc}</div>
  <div>
    {lbl("Styles nommés du modèle")}
    {tbl([["S360 Titre", "Unbounded Regular 22 pt, Nuit spatiale", "Titre du document"], ["S360 Titre 1", "Unbounded Medium 15 pt", "Partie"], ["S360 Titre 2", "Manrope Bold 8 pt, capitales", "Section"],
          ["S360 Corps", "Manrope Regular 10 / 15 pt", "Texte courant"], ["S360 Liste", "point en dégradé, retrait 5 mm", "Énumération"], ["S360 Tableau", "filets horizontaux seuls", "Données"], ["S360 Légende", "Manrope Regular 8 pt, Ardoise", "Sources, notes"]],
         head=["Style", "Réglage", "Usage"], widths=["24%", "48%", "28%"])}
    <div style="margin-top:6mm">{blk("Règles", bul(["Aucune mise en forme manuelle&nbsp;: uniquement les styles nommés", "Tableaux sans trame ni bordure verticale", "Verdana et Arial en substitution si les polices ne sont pas installées", "Export PDF systématique pour tout envoi externe"]))}</div>
  </div>
</div>""")

# =================================================================== 29 catalogue
cat_cover = (f'<div class="mk mk-dark shadow" style="width:62mm;height:87.7mm;padding:6mm 5.5mm">'
             f'<div style="position:absolute;right:-18mm;bottom:-14mm">{logo("orbite-neg", "62mm")}</div>'
             f'{logo("logotype-neg", "22mm", style="position:relative")}'
             f'<p style="position:relative;margin-top:14mm;font:400 10pt/1.05 var(--d);letter-spacing:-.025em">Catalogue<br>des formations</p>'
             f'<p style="position:relative;margin-top:2.4mm;font:600 9pt/1 var(--d)" class="grad-neg">2027</p></div>')
cat_chap = (f'<div class="mk mk-fumee shadow" style="width:62mm;height:87.7mm;padding:7mm 5.5mm">'
            f'<p style="font:600 19pt/1 var(--d);background:{GPOS};-webkit-background-clip:text;background-clip:text;color:transparent">02</p>'
            f'<p style="margin-top:4mm;font:400 8pt/1.12 var(--d);letter-spacing:-.02em">Digital &amp;<br>intelligence<br>artificielle</p>'
            f'<div style="margin-top:5mm">{icon("ia", "7mm", ORBITE)}</div>'
            f'<p style="position:absolute;left:5.5mm;right:5.5mm;bottom:7mm;font:300 4.4pt/1.45 var(--d);color:{ARDOISE}">«&nbsp;Comprendre l\'outil, puis apprendre à s\'en servir.&nbsp;»</p></div>')
fiche_sec = lambda t, n: f'{k(t, "2.8pt", ORBITE, extra="margin-top:2.2mm")}<div style="margin-top:.8mm">{lines(n, [100, 94, 88])}</div>'
cat_fiche = (f'<div class="mk mk-white shadow" style="width:62mm;height:87.7mm;padding:5.5mm 5.5mm">'
             f'{k("Digital &amp; IA · Réf. [—]", "2.8pt", ARDOISE)}'
             f'<p style="margin-top:1.4mm;font:500 6pt/1.15 var(--d);letter-spacing:-.01em">L\'IA générative au quotidien</p>'
             f'<div style="display:flex;gap:1.2mm;margin-top:2mm;flex-wrap:wrap">' + "".join(f'<span style="font:700 2.6pt/1 var(--t);padding:.9mm 1.4mm;border-radius:1mm;background:{FUMEE}">{t}</span>' for t in ("2 jours · 14 h", "Présentiel ou distanciel", "Inter · intra")) + '</div>'
             f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 3mm">'
             f'<div>{fiche_sec("Objectifs", 3)}{fiche_sec("Public et prérequis", 2)}{fiche_sec("Méthodes", 2)}{fiche_sec("Évaluation", 2)}</div>'
             f'<div>{fiche_sec("Programme", 7)}{fiche_sec("Accessibilité", 2)}{fiche_sec("Délais et tarif", 2)}</div></div>'
             f'<div style="position:absolute;right:5.5mm;bottom:4.6mm">{prog_ring("5mm", 1, dark=False)}</div></div>')
page("Catalogue de formations", "Édition", f"""
<div class="g" style="grid-template-columns:62mm 62mm 62mm 1fr;gap:6mm;margin-top:-3mm">
  <div>{lbl("Couverture")}{cat_cover}</div>
  <div>{lbl("Ouverture de domaine")}{cat_chap}</div>
  <div>{lbl("Fiche programme")}{cat_fiche}</div>
  <div>
    {lbl("Fabrication")}
    {tbl([["Format", "A4, 210 × 297 mm"], ["Couverture", "300 g/m², soft touch"], ["Intérieur", "115 g/m², couché mat"], ["Façonnage", "dos carré collé"]], widths=["38%", "62%"])}
    <p class="cap" style="margin-top:3mm">Chaque domaine ouvre sur son numéro en dégradé et son icône. Version PDF interactive pour le site.</p>
  </div>
</div>
<div class="note" style="margin-top:7mm"><b>Fiche programme.</b> Chaque fiche présente objectifs, public et prérequis, durée, modalités et délais d'accès, tarif, méthodes, modalités d'évaluation, accessibilité aux personnes en situation de handicap et contact. Liste à valider avec le responsable qualité au regard du référentiel national qualité {V}. Aucun taux de satisfaction ou de réussite n'est publié sans source datée.</div>""")

# =================================================================== 30 attestation
page("Attestation de fin de formation", "Édition", f"""
<div class="g" style="grid-template-columns:142mm 1fr;gap:12mm;margin-top:-2mm">
  <div>{lbl("Modèle A4 paysage")}{certificate()}</div>
  <div>
    {blk("Composition", bul(["Logo principal en haut à gauche, 44 mm", "Titre en Unbounded Regular, nom de l'apprenant en Unbounded Medium", "Orbite en filigrane, Nuit spatiale à 6&nbsp;%", "Fond Fumée blanche, aucune bordure décorative"]))}
    {blk("Production", txt("Généré depuis la plateforme de gestion des formations, en PDF signé. Version imprimée sur 250 g/m² couché mat pour les remises en main propre."))}
    {blk("Mentions", txt(f"Intitulé, dates, durée, modalité, résultat de l'évaluation des acquis. Les mentions obligatoires et la distinction avec le certificat de réalisation sont à valider {V}."))}
  </div>
</div>""")

# =================================================================== 31 site internet
page("Site internet", "Digital", f"""
<div class="g" style="grid-template-columns:150mm 44mm 1fr;gap:7mm;align-items:start;margin-top:-3mm">
  <div>{lbl("Landing — ordinateur")}{browser("img/site-desktop.jpg", "150mm")}<p class="cap">Le logo s'écrit à l'ouverture (voir page 22), puis la promesse et les appels à l'action apparaissent.</p></div>
  <div>{lbl("Mobile")}{phone('<img src="img/site-mobile.jpg">', 44, 93)}</div>
  <div>
    {lbl("Système d'interface")}
    {tbl([["Conteneur", "1 240 px · 12 col. · 24 px"], ["Titres", "Unbounded Medium 64 / 40 px"], ["Texte", "Manrope 17 / 27 px"], ["Boutons", "pilule, #2D69FC, libellé blanc"], ["Cartes", "rayon 20 px, filet 1 px"], ["Animation", "GSAP&nbsp;: intro du logo, ScrollTrigger"]], widths=["34%", "66%"])}
    <div style="margin-top:4mm">{blk("Exigences", bul(["Accessibilité WCAG 2.1 AA, contrastes page 15", "«&nbsp;Réduire les animations&nbsp;» respecté", f"Mentions légales, confidentialité et cookies conformes RGPD {V}", "Aucun chiffre ni label affiché sans justificatif"]))}</div>
  </div>
</div>""")

# =================================================================== 32 réseaux sociaux
li = (f'<div class="tile tile--blanc" style="display:block;place-items:normal;height:auto;padding:0;overflow:hidden">'
      f'<div class="mk mk-dark" style="height:25.4mm;display:flex;align-items:center;justify-content:flex-end;padding-right:10mm">'
      + rings(880, 500, [300, 420, 560], style="position:absolute", sats=[(420, 250, 8, HALO)])
      + f'<p style="position:relative;font:700 4.6pt/1 var(--t);letter-spacing:.3em;color:{HALO}">DÉVELOPPER SES COMPÉTENCES À 360°</p></div>'
      f'<div style="position:relative;padding:0 6mm 5mm">'
      f'<div style="width:17mm;height:17mm;margin-top:-8.5mm;border-radius:1.4mm;background:{NUIT};border:1mm solid #fff;display:grid;place-items:center">{logo("orbite-neg", "10mm")}</div>'
      f'<p style="margin-top:2mm;font:700 7.4pt/1.2 var(--t)">Skill360</p><p style="font:500 5.6pt/1.3 var(--t);color:{ARDOISE}">Centre de formation · Formation &amp; développement des compétences</p></div></div>')
story = (f'<div class="mk mk-dark shadow" style="width:34mm;height:60.4mm;border-radius:1mm;padding:5mm 3.6mm">'
         + rings(500, 760, [260, 360], style="position:absolute")
         + f'{logo("logotype-neg", "15mm", style="position:relative")}'
         f'<p style="position:relative;margin-top:16mm;font:400 6.4pt/1.12 var(--d);letter-spacing:-.02em">Inscriptions ouvertes</p>'
         f'<p style="position:relative;margin-top:1.4mm;font:600 3.6pt/1.4 var(--t);color:{BRUME}">Sessions de janvier</p>'
         f'<div style="position:absolute;left:3.6mm;right:3.6mm;bottom:5mm;height:5mm;border-radius:2.5mm;background:{C["orbite"]};display:grid;place-items:center;font:700 3.4pt/1 var(--t)">En savoir plus</div></div>')
page("Réseaux sociaux", "Digital", f"""
<div class="g" style="grid-template-columns:1.25fr 1fr;gap:10mm;margin-top:-3mm">
  <div>
    {lbl("Page entreprise")}{li}
    <div style="margin-top:6mm">{lbl("Publications — 1 200 × 1 200 px")}
      <div style="display:flex;gap:4mm">{social_post("dark")}{social_post("light")}{social_post("indigo")}</div></div>
  </div>
  <div>
    <div style="display:flex;gap:6mm"><div>{lbl("Story — 9:16")}{story}</div>
      <div>{lbl("Ligne éditoriale")}{txt("Trois registres seulement&nbsp;: <b>sessions</b> (dates, nouvelles formations), <b>parcours</b> (témoignages, avec accord écrit), <b>conseils</b> (fiches pratiques).")}
      <div style="margin-top:3mm">{bul(["Un visuel = un message", "Pas d'emoji dans les visuels", "#Skill360 + deux mots-dièse sectoriels au plus", "Témoignage publié uniquement avec accord écrit"])}</div></div></div>
    <div style="margin-top:5mm">{tbl([["Avatar", "Orbite sur carré Nuit, 400 × 400 px"], ["Bannière", "1 128 × 191 px, Nuit + arcs d'orbite"], ["Publications", "1 200 × 1 200 px · 1 080 × 1 350 px"], ["Story", "1 080 × 1 920 px, zones de sécurité 250 px"]], widths=["30%", "70%"])}</div>
  </div>
</div>""")

# =================================================================== 33 plateforme e-learning
icons_app = (f'<div style="display:flex;gap:4mm;align-items:flex-end">'
             f'<img src="logos/skill360-icone-app.svg" style="width:20mm;border-radius:4.4mm">'
             f'<img src="logos/skill360-icone-app.svg" style="width:12mm;border-radius:2.7mm">'
             f'<img src="logos/skill360-favicon.svg" style="width:7mm;border-radius:1.6mm"></div>')
page("Plateforme e-learning", "Digital", f"""
<div class="g" style="grid-template-columns:40mm 40mm 40mm 1fr;gap:7mm;margin-top:-3mm">
  <div>{lbl("Lancement")}{phone(app_launch())}</div>
  <div>{lbl("Mes parcours")}{phone(app_list())}</div>
  <div>{lbl("Module")}{phone(app_module())}</div>
  <div>
    {lbl("Icône d'application")}{icons_app}
    <p class="cap">Orbite sur carré Nuit spatiale. Fournir le fichier à bords carrés, 1 024 × 1 024 px&nbsp;: le système applique lui-même l'arrondi. Version aplat sous 32 px.</p>
    <div style="margin-top:5mm">{lbl("Interface")}{tbl([["Base", "8 pt"], ["Cible tactile", "44 × 44 pt minimum"], ["Accent", "Halo cyan, état actif uniquement"], ["Progression", "anneau à trois segments&nbsp;: savoir, savoir-faire, savoir-être"]], widths=["34%", "66%"])}</div>
    <p class="cap" style="margin-top:3mm">Périmètre fonctionnel, hébergement et conformité RGPD de la plateforme {V}.</p>
  </div>
</div>""")

# =================================================================== 34 signalétique
wall = (f'<div class="mk shadow" style="width:150mm;height:80mm;border-radius:1mm;background:linear-gradient(180deg,#141A36,{NUIT});display:grid;place-items:center">'
        + rings(500, 520, [260, 360, 470], style="position:absolute", sats=[(360, 60, 6, HALO)])
        + f'<div style="position:relative;filter:drop-shadow(0 .6mm .4mm rgba(0,0,0,.6))">{logo("logo-h-neg", "100mm")}</div>'
          f'<p style="position:absolute;right:5mm;bottom:4mm;font:700 3.6pt/1 var(--t);letter-spacing:.24em;color:{BRUME}">ACCUEIL — LETTRES DÉCOUPÉES, ALUMINIUM ANODISÉ</p></div>')
page("Signalétique", "Environnement", f"""
<div class="g" style="grid-template-columns:150mm 1fr;gap:10mm;margin-top:-3mm">
  <div>{lbl("Mur d'accueil")}{wall}</div>
  <div>{lbl("Plaque de salle")}{plaque(84)}</div>
</div>
<div class="g g3" style="margin-top:8mm;gap:10mm">
  {blk("Matériaux", txt("Lettres découpées en aluminium anodisé ou Dibond Nuit spatiale, impression UV, entretoises de 15 mm, fixations invisibles."))}
  {blk("Principes", bul(["Réserve portée à 2X", "Salles nommées d'après les valeurs&nbsp;: Exploration, Excellence, Accompagnement, Ouverture", "Pictogrammes issus du jeu d'icônes de la marque"]))}
  {blk("Accessibilité", txt(f"Hauteurs de pose, contrastes et lisibilité à vérifier selon la réglementation applicable aux établissements recevant du public {V}."))}
</div>""")

# =================================================================== 35 enseigne
page("Enseigne", "Environnement", f"""
{lbl("Façade — lettres boîtiers rétroéclairées")}{facade()}
<div class="g g3" style="margin-top:8mm;gap:10mm">
  {blk("Exécution", tbl([["Type", "lettres boîtiers découpées"], ["Skill", "face opale, blanc 4 000 K"], ["360", "face Halo cyan, version aplat"], ["Réserve", "2X"]], widths=["32%", "68%"]))}
  {blk("Composition", bul(["Logotype seul, sans signature", "Le dégradé ne se reproduit pas en enseigne&nbsp;: version aplat", "Pas de caisson lumineux plein ni de contour néon"]))}
  {blk("Autorisations", txt(f"Déclaration ou autorisation préalable selon la commune, règlement local de publicité, horaires d'extinction&nbsp;: à instruire avant commande {V}."))}
</div>""")

# =================================================================== 36 salons
stand = (f'<div class="mk shadow" style="width:118mm;height:84mm;border-radius:1mm;background:linear-gradient(180deg,#E9EDF5,#D8DEEA)">'
         f'<div style="position:absolute;left:8mm;right:8mm;top:6mm;height:50mm;background:{NUIT};border-radius:.6mm;overflow:hidden;display:grid;place-items:center">'
         + rings(500, 500, [260, 360, 470], style="position:absolute", sats=[(360, 70, 7, HALO)])
         + f'{logo("logo-h-neg", "70mm", style="position:relative")}</div>'
           f'<div style="position:absolute;left:38mm;width:42mm;bottom:6mm;height:24mm;background:{FUMEE};border-radius:.6mm;display:grid;place-items:center;box-shadow:0 1mm 2mm rgba(7,11,31,.2)">{logo("orbite", "12mm")}</div></div>')
badge = (f'<div class="mk mk-white shadow" style="width:32mm;height:46mm;border-radius:1mm;padding:4mm 3.4mm">'
         f'<div style="position:absolute;left:0;right:0;top:0;height:12mm;background:{NUIT};display:grid;place-items:center">{logo("logotype-neg", "16mm")}</div>'
         f'<p style="margin-top:12mm;font:500 6pt/1.15 var(--d)">Prénom<br>Nom</p>{k("Formateur", "3.2pt", ORBITE, extra="margin-top:1.4mm")}'
         f'<span style="position:absolute;left:3.4mm;bottom:4mm;width:8mm;height:.8pt;background:{GPOS}"></span></div>')
page("Salons et événements", "Événementiel", f"""
<div class="g" style="grid-template-columns:36mm 118mm 32mm 1fr;gap:8mm;align-items:start;margin-top:-3mm">
  <div>{lbl("Kakémono")}{kakemono(34)}</div>
  <div>{lbl("Stand 3 × 2,5 m")}{stand}</div>
  <div>{lbl("Badge")}{badge}</div>
  <div>
    {lbl("Réglages")}
    {tbl([["Kakémono", "85 × 200 cm, logo en tête"], ["Stand", "fond Nuit, comptoir Fumée"], ["Réserve", "2X sur tous les supports"], ["Lisibilité", "logo visible à 10 m"]], widths=["38%", "62%"])}
    <p class="cap" style="margin-top:3mm">Le message tient en une phrase. Le bas des visuels (sous 80 cm) ne porte aucune information&nbsp;: il est masqué par le public.</p>
  </div>
</div>""")

# =================================================================== 37 objets & textile
notebook = (f'<div class="mk mk-fumee shadow" style="width:40mm;height:56mm;border-radius:.6mm 1.4mm 1.4mm .6mm;display:grid;place-items:center">'
            f'<div style="position:absolute;left:0;top:0;bottom:0;width:2.2mm;background:{NUIT}"></div>{logo("logo-sq", "22mm")}'
            f'<span style="position:absolute;right:5mm;top:0;width:2.4mm;height:12mm;background:{ORBITE}"></span></div>')
mug = (f'<div style="position:relative;width:46mm;height:44mm">'
       f'<div style="position:absolute;right:0;top:9mm;width:14mm;height:20mm;border:2.4mm solid {NUIT};border-radius:0 7mm 7mm 0"></div>'
       f'<div class="shadow" style="position:absolute;left:0;top:0;width:36mm;height:44mm;background:{NUIT};border-radius:.8mm .8mm 4mm 4mm;display:grid;place-items:center">{logo("orbite-neg", "16mm", n360=HALO)}</div></div>')
tee = (f'<div style="position:relative;width:56mm;height:56mm">'
       f'<div class="shadow" style="position:absolute;inset:0;background:{NUIT};clip-path:polygon(28% 0,40% 6%,60% 6%,72% 0,100% 16%,90% 38%,80% 33%,80% 100%,20% 100%,20% 33%,10% 38%,0 16%);border-radius:1mm"></div>'
       f'<div style="position:absolute;left:33mm;top:16mm">{logo("orbite-neg", "7mm", n360=HALO)}</div></div>')
page("Objets et textile", "Événementiel", f"""
<div class="g g4" style="gap:8mm">
  {"".join(f'<div><div style="height:62mm;display:flex;align-items:flex-end;justify-content:center;padding-bottom:2mm;border-bottom:.5pt solid var(--ligne)">{obj}</div><p class="sw-n" style="margin-top:2.6mm">{t}</p><p class="cap" style="margin-top:.6mm">{c}</p></div>' for obj, t, c in [(tote(46), "Tote bag", "Coton bio 280 g, sérigraphie deux couleurs."), (notebook, "Carnet de l'apprenant", "A5, couverture Fumée, signet Bleu orbite."), (mug, "Mug", "Céramique Nuit, Orbite aplat Halo cyan."), (tee, "Textile formateurs", "Orbite brodée côté cœur, 7 cm.")])}
</div>
<div class="g g3" style="margin-top:9mm;gap:10mm">
  {blk("Marquage", txt("Sérigraphie, broderie, gravure et tampographie utilisent la <b>version aplat</b>&nbsp;: «&nbsp;360&nbsp;» Halo cyan sur fond sombre, Bleu orbite sur fond clair. Le dégradé est réservé à l'impression quadri."))}
  {blk("Choix des objets", txt("Peu d'objets, utiles à la formation&nbsp;: carnet, sac, gourde, textile des formateurs. Les objets jetables ne portent pas la marque."))}
  {blk("Interdit", bul(["Le dégradé en broderie ou en sérigraphie", "Le logotype sur une surface courbe de moins de 30 mm", "Les couleurs d'objet hors Nuit, Fumée, blanc ou noir"], "bul--x"))}
</div>""")

# =================================================================== 38 co-signature & labels
partner = '<div style="width:34mm;height:13mm;border:.6pt dashed #AEB8D2;border-radius:1mm;display:grid;place-items:center;font:700 3.6pt/1 var(--t);letter-spacing:.2em;color:#4A5170">LOGO PARTENAIRE</div>'
label_box = '<div style="width:24mm;height:16mm;border:.6pt dashed #AEB8D2;border-radius:1mm;display:grid;place-items:center;text-align:center;font:700 3.2pt/1.5 var(--t);letter-spacing:.16em;color:#4A5170;padding:1mm">MARQUE DE<br>CERTIFICATION<br>FICHIER OFFICIEL</div>'
page("Co-signature et labels", "Gouvernance", f"""
<div class="g" style="grid-template-columns:1.15fr 1fr;gap:12mm">
  <div>
    {lbl("Co-signature avec un partenaire ou un client")}
    <div class="tile tile--blanc" style="height:34mm;display:flex;align-items:center;justify-content:center;gap:9mm">{logo("logotype", "46mm")}<span style="width:.6pt;height:14mm;background:#C9D0E2"></span>{partner}</div>
    <p class="cap">Skill360 à gauche, filet vertical de 0,5 pt, réserve X de part et d'autre. Hauteurs optiquement égales.</p>
    <div style="margin-top:6mm">{lbl("Labels, certifications et financeurs")}
    <div class="tile tile--fumee" style="height:34mm;display:flex;align-items:center;justify-content:space-between;padding:0 9mm">{logo("logo-h", "62mm")}<div style="display:flex;gap:4mm">{label_box}{label_box}</div></div>
    <p class="cap">Les marques tierces se placent en pied de page, alignées à droite, sur fond clair et dans leurs propres couleurs.</p></div>
  </div>
  <div>
    {lbl("Règles")}
    {tbl([["Ordre", "Skill360 en premier, sauf document édité par le partenaire"], ["Taille", "marques de hauteurs optiquement égales"], ["Séparation", "filet vertical 0,5 pt, réserve X"], ["Fichiers", "uniquement les fichiers officiels des organismes"], ["Mentions", "selon les règles d'usage de chaque marque"]], widths=["28%", "72%"])}
    <div style="margin-top:6mm">{blk("Interdit", bul(["Afficher une certification ou un label sans certificat en cours de validité", "Associer une marque de certification à une action hors de son périmètre", "Recolorer ou redessiner une marque tierce", "Décliner l'Orbite dans les couleurs d'un partenaire"], "bul--x"))}</div>
    <p class="cap" style="margin-top:3mm">Conditions d'usage des marques de certification et des dispositifs de financement à valider avec le responsable qualité {V}.</p>
  </div>
</div>""", lead="Skill360 signe seul ses supports. Quand une autre marque apparaît, elle s'ajoute selon des règles fixes, sans jamais s'imbriquer dans le logo.")

# =================================================================== 39 ensemble des applications
def ov(inner, bg="fumee", st=""):
    return f'<div class="tile tile--{bg}" style="height:58mm;{st}">{inner}</div>'


page("Ensemble des applications", "Annexes", f"""
<div class="g g4 gap-s">
  {ov(card_recto(56, 36.2), "fumee")}
  {ov('<img src="logos/skill360-icone-app.svg" style="width:30mm;border-radius:6.6mm" class="shadow">', "blanc")}
  {ov(kakemono(22), "fumee")}
  {ov(tote(36), "blanc")}
  {ov(social_post("dark", 40), "fumee")}
  {ov(plaque(60), "blanc")}
  {ov(slide("cover", 54), "fumee")}
  {ov(browser("img/site-desktop.jpg", "56mm"), "blanc")}
</div>
<p class="cap" style="margin-top:4mm">Maquettes vectorielles produites depuis les fichiers de la charte, à l'échelle. Aucun support n'a encore été fabriqué&nbsp;: les photographies de mise en situation seront faites sur les premiers tirages {V}.</p>""")

# =================================================================== 40 récapitulatif
rules = ["Le logo ne se redessine pas&nbsp;: il s'emploie depuis les fichiers fournis.",
         "L'Orbite tourne dans le sens horaire, et seulement en mouvement.",
         "Les échappements de l'Orbite ne se comblent jamais.",
         "Le dégradé n'appartient qu'au «&nbsp;360&nbsp;» et au point&nbsp;; la lumière ne dépasse pas 8&nbsp;% d'une surface.",
         "Unbounded pour le logotype et les titres, Manrope pour tout le reste.",
         "Sous 32 px ou en une couleur, on passe à la version aplat.",
         "Aucun chiffre, aucun label, aucune mention légale sans pièce justificative."]
rl = "".join(f'<div class="toc__row" style="grid-template-columns:10mm 1fr;padding:2.1mm 0"><i>{i + 1:02d}</i><span style="font-weight:500">{r}</span></div>' for i, r in enumerate(rules))
tree = """SKILL360_Identite/
├── 01_Charte_graphique/    PDF + source HTML
├── 02_Logo/                SVG · PNG · favicons
├── 03_Couleurs/            CSS · JSON
├── 04_Typographies/        Unbounded · Manrope · licences OFL
├── 05_Papeterie/           carte de visite · en-tête · attestation
├── 06_Digital/             signature e-mail · réseaux sociaux
└── 07_Site_Web/            site · animation du logo (GSAP)"""
page("Récapitulatif", "Annexes", f"""
<div class="g" style="grid-template-columns:1.1fr 1fr;gap:14mm">
  <div>{lbl("Les sept règles")}{rl}</div>
  <div>
    {lbl("Livrables")}
    <pre style="margin:0;padding:5mm 6mm;background:var(--fumee);border-radius:1.6mm;font:500 6.4pt/1.75 Consolas, monospace;color:var(--nuit);white-space:pre">{tree}</pre>
    <div style="margin-top:9mm;display:flex;justify-content:center">{logo("logo-h", "92mm")}</div>
  </div>
</div>""")

# =================================================================== 41 points à valider
pts = [["04 · 24", "Raison sociale, SIRET, déclaration d'activité, certification qualité", "Direction"],
       ["14", "Références Pantone, profils ICC, épreuves du dégradé", "Imprimeur"],
       ["15 · 31", "Adoption de la valeur interface #2D69FC pour les boutons", "Direction artistique"],
       ["18", "Reportage photographique et autorisations", "Direction"],
       ["23 · 26", "Fonctions, téléphones, adresses e-mail", "Direction"],
       ["25", "Cotes de fenêtre et zones réservées", "Opérateur postal"],
       ["29 · 30", "Contenu des fiches programmes et de l'attestation", "Responsable qualité"],
       ["31 · 33", "Mentions légales, RGPD, cookies, hébergement", "Conseil juridique"],
       ["35", "Enseigne&nbsp;: règlement local de publicité", "Mairie · fabricant"],
       ["38", "Usage des marques de certification et de financement", "Responsable qualité"]]
page("Points à valider avant diffusion", "Annexes", f"""
<div class="g" style="grid-template-columns:1.25fr 1fr;gap:12mm">
  <div>{tbl(pts, head=["Page", "Point à arrêter", "Responsable"], widths=["14%", "60%", "26%"])}</div>
  <div>
    {lbl("Points juridiques")}
    {bul(["<b>Disponibilité du nom.</b> Recherche d'antériorité sur «&nbsp;Skill360&nbsp;» et sur le logotype, en particulier en classe 41 (éducation, formation), puis dépôt avant toute diffusion large.",
          "<b>Nom de domaine.</b> skill360.fr figure sur les supports à titre d'exemple&nbsp;: réservation à confirmer avant impression.",
          "<b>Polices.</b> Unbounded et Manrope sont sous licence SIL OFL&nbsp;: usage commercial et intégration dans un logo autorisés.",
          "<b>GSAP.</b> Bibliothèque et plugins (MorphSVG, DrawSVG, SplitText) gratuits depuis la version 3.13, sous licence «&nbsp;Standard No Charge&nbsp;»&nbsp;: conditions à relire avant mise en ligne."])}
    <div style="margin-top:6mm">{blk("Gouvernance de la marque", txt("Un responsable de marque unique détient les fichiers sources et valide toute nouvelle application. Les prestataires reçoivent des fichiers d'exécution, jamais les sources modifiables."))}</div>
  </div>
</div>""", lead="Cette charte est la version 1.0. Les éléments marqués [À&nbsp;VÉRIFIER] doivent être arrêtés avant toute diffusion externe.")


# =================================================================== 42 dos
def back(n):
    return (f'<section class="page cover" id="p{n}">'
            + rings(500, 500, [200, 290, 390, 510], style="position:absolute", sats=[(290, 52, 5, HALO), (510, 236, 6, ORBITE)])
            + '<div class="halo" style="width:150mm;height:150mm;left:73.5mm;top:20mm"></div>'
            + f'<div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);display:grid;justify-items:center;gap:9mm">'
              f'{logo("orbite-neg", "44mm")}<p style="font:300 15pt/1 var(--d);letter-spacing:-.02em;color:var(--fumee)">Entrez dans l\'orbite.</p></div>'
            + '<div class="cover__foot"><div><p class="cover__meta" style="margin:0">Skill360 — Charte graphique · V1.0 · Octobre 2026</p></div>'
              '<div class="cover__sig">Formation &amp; développement des compétences</div></div></section>')


raw_page(back, "Dos", "")
