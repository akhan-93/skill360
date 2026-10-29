# Skill360 — site vitrine

Site statique issu de la maquette **Piste D — Visages × Parcours**.
Aucune dépendance ni étape de build : ouvrir `index.html` dans un navigateur suffit.

## Pages

| Fichier | Page |
|---|---|
| `index.html` | Accueil |
| `formations.html` | Formations — landing & catégories |
| `categorie-management-leadership.html` | Catégorie « Management & leadership » |
| `fiche-manager-equipe.html` | Fiche formation « Manager une équipe au quotidien » |

## Arborescence

```
*.html                  pages du site
assets/css/site.css     design system (couleurs, typo, composants, responsive)
assets/js/site.js       interactions (vanilla JS, sans dépendance)
assets/img/             logos et photos (versions web)
archive/v1/             ancienne version du site (+ scripts de build / charte)
```

Polices chargées depuis Google Fonts : Bricolage Grotesque, Instrument Sans, JetBrains Mono.

Couleurs : bleu `#2F5FE8` (principale) et orange `#FF7A3D` (secondaire, variables `--warm*` dans `site.css`).
L’orange porte le diagnostic (boutons, questionnaire), les objectifs (pointillés des radars), l’e-learning, la carte, et ce qui demande l’attention (populaire, places limitées, sur-mesure). Les points `•` en fin de titre sont orange.
En texte sur fond clair, utiliser `--warm-ink` (`#C2410C`) pour respecter le contraste AA ; sur un bouton orange, le texte est bleu nuit.

## Interactions

- **Diagnostic 360** : tous les boutons « Faire un diagnostic » ouvrent un questionnaire en 6 questions ; le radar se redessine à chaque réponse et une catégorie est recommandée.
- **Formulaire de contact** : « Nous contacter », « Être rappelé », « S’inscrire », « Devis »… ouvrent un tiroir pré-rempli selon le contexte.
- **E-learning** (accueil) : lecteur de démo — lecture/pause, choix de la leçon, progression du module.
- **Carte de France** (accueil) : 3 modes (sessions en ville, dans vos locaux, à distance) ; survol ou clic sur une ville pour afficher sa zone et ses sessions.
- **Catalogue** : recherche avec suggestions et filtres par format.
- **Catégorie** : filtres (format, durée, niveau), tri, recherche via `?q=…`.
- **Fiche** : programme en accordéon, radar avant/après, barre d’inscription collante.
- **Partout** : en-tête qui se masque au scroll, menu mobile, apparitions au scroll, curseur-aperçu sur la liste des formations, carrousel de témoignages, transitions entre pages.
- `prefers-reduced-motion` est respecté ; le contenu reste lisible si le JavaScript ne se charge pas.

## À configurer avant mise en ligne

- **Envoi du formulaire** : renseigner `CONTACT_ENDPOINT` en haut de `assets/js/site.js` (Formspree, API…). Tant qu’il est vide, le formulaire fonctionne en **mode démo** (confirmation affichée, rien n’est envoyé).
- **Contenus entre crochets** : `[Intitulé formation existante 1]`, `[000]+`, `[0 000] €`, `[JJ/MM]`, `[TÉLÉPHONE]`, témoignages, etc.
- **Programme de la fiche** : les points des modules 02 à 04 sont des propositions entre crochets, à valider.
- **Villes de la carte** : la liste (16 villes, une par région au minimum) est un exemple. Elle se modifie dans `index.html` (boutons `.city-chip` avec `data-lat` / `data-lon` / `data-region`) ; les épingles suivent automatiquement. Les dates et nombres de sessions affichés sont des placeholders (`[JJ/MM]`, `[0]`) dans le module « Carte de France » de `site.js`.
- **E-learning** : le lecteur est une démonstration visuelle (leçons d’exemple, pas de vraie vidéo) ; « Demander un accès démo » ouvre le formulaire de contact.
- L’année du pied de page est mise à jour automatiquement.

## Hors dépôt (`../_sources/`)

- `maquette-D-export/` — export brut de l'outil de design.
- `photos-hd/` — photos originales haute définition.
