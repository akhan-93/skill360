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

## Interactions

- **Diagnostic 360** : tous les boutons « Faire un diagnostic » ouvrent un questionnaire en 6 questions ; le radar se redessine à chaque réponse et une catégorie est recommandée.
- **Formulaire de contact** : « Nous contacter », « Être rappelé », « S’inscrire », « Devis »… ouvrent un tiroir pré-rempli selon le contexte.
- **Catalogue** : recherche avec suggestions et filtres par format.
- **Catégorie** : filtres (format, durée, niveau), tri, recherche via `?q=…`.
- **Fiche** : programme en accordéon, radar avant/après, barre d’inscription collante.
- **Partout** : en-tête qui se masque au scroll, menu mobile, apparitions au scroll, curseur-aperçu sur la liste des formations, carrousel de témoignages, transitions entre pages.
- `prefers-reduced-motion` est respecté ; le contenu reste lisible si le JavaScript ne se charge pas.

## À configurer avant mise en ligne

- **Envoi du formulaire** : renseigner `CONTACT_ENDPOINT` en haut de `assets/js/site.js` (Formspree, API…). Tant qu’il est vide, le formulaire fonctionne en **mode démo** (confirmation affichée, rien n’est envoyé).
- **Contenus entre crochets** : `[Intitulé formation existante 1]`, `[000]+`, `[0 000] €`, `[JJ/MM]`, `[TÉLÉPHONE]`, témoignages, etc.
- **Programme de la fiche** : les points des modules 02 à 04 sont des propositions entre crochets, à valider.
- L’année du pied de page est mise à jour automatiquement.

## Hors dépôt (`../_sources/`)

- `maquette-D-export/` — export brut de l'outil de design.
- `photos-hd/` — photos originales haute définition.
