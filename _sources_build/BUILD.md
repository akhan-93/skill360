# Skill360 — chaîne de production

Régénère le logo, le site, la charte et les supports de `SKILL360_Identite/`.
Toutes les commandes se lancent depuis ce dossier (`_sources_build`).

## Prérequis (une fois)

```bash
py -m venv venv
venv/Scripts/python -m pip install fonttools brotli uharfbuzz pillow pymupdf
cd tools && npm install && cd ..        # puppeteer-core (pilote Chrome installé) + gsap
```

Chrome doit être installé dans `C:/Program Files/Google/Chrome/Application/` (chemin codé dans `tools/*.js`).

## Ordre de génération

```bash
PY=venv/Scripts/python
OUT="../SKILL360_Identite"

$PY make_webfonts.py dl_fonts build/fonts                                          # polices web WOFF2
$PY build_logo.py . dl_fonts/Unbounded-VF.ttf dl_fonts/Manrope-VF.ttf build         # géométrie, SVG, sprite
$PY colors.py build/colors.json                                                    # palette, contrastes
$PY build_charte.py .                                                              # charte.html (+ polices et logos dans charte/)
$PY export_supports.py . "$OUT" && node tools/render_jobs.js charte/exports/jobs.json   # PNG, PDF, og-image
$PY build_site.py . build/logo_data.json site_src build "$OUT/07_Site_Web"          # site
node tools/print_pdf.js charte/charte.html charte/charte.pdf charte/png             # PDF de la charte + aperçus
$PY package_deliverables.py . "$OUT"                                               # copie dans la livraison
```

L'ordre compte : `export_supports.py` utilise les polices et logos copiés par `build_charte.py`,
et produit `og-image.png` et les icônes que `build_site.py` embarque.

## Où modifier quoi

| Sujet | Fichier |
| --- | --- |
| Dessin de l'Orbite (diamètre, épaisseur, coupes, chevron, point) | `build_logo.py` (constantes `U`, `T`, `GAP`, `TIP`, `DOT`, `CUTS`) |
| Couleurs et dégradés du logo | `build_logo.py` (`C`, `GRAD_POS`, `GRAD_NEG`), `colors.py` |
| Contenus et mise en page du site | `site_src/index.src.html`, `site_src/assets/css/style.css` |
| Animation GSAP du logo | `site_src/assets/js/logo-intro.js` |
| Animations au scroll | `site_src/assets/js/main.js` |
| Pages de la charte | `charte_p1.py` (fondations, identité, système), `charte_p2.py` (applications, annexes) |

Les images de la page Motion et de la page Site internet (`charte/img/`) sont des captures du site :
les refaire avec `tools/frames.js` et `tools/shot.js` après une modification de l'animation ou du site.
