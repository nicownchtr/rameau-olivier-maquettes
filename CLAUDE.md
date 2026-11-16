# Maquettes de refonte — Le Rameau d'Olivier

Maquettes HTML statiques de la refonte de https://rameau-olivier.fr/ (épicerie fine, 12 rue de Pologne,
78100 Saint-Germain-en-Laye). Le patron a retenu la **proposition 3 « Nuit gourmande »**, base du futur thème WordPress.
Les autres propositions ont été supprimées ; la 6 reste comme reproduction du site actuel, pour comparer.

- En ligne : https://nicownchtr.github.io/rameau-olivier-maquettes/ (GitHub Pages, branche `main`, racine du dépôt).
- Chaque push sur `main` est publié automatiquement en 1 à 2 minutes.
- Le propriétaire pilote souvent ces modifications **depuis son téléphone** : réponds en français, de façon courte,
  et termine toujours par les liens directs vers les pages modifiées.

## Mémoire partagée : `NOTES.md`

@NOTES.md

`NOTES.md` est la mémoire commune aux sessions locales et cloud. À chaque demande :
- mettre à jour « État actuel » ou « Exigences » si quelque chose change ;
- ajouter une ligne en haut du « Journal » ;
- tout cela dans le même commit que la modification.

Ne rien y mettre de privé : le dépôt est public.

## Structure

| Chemin | Rôle |
|---|---|
| `outils/generer.py` | **Source des pages** : en-tête, menu, pied de page, contenu de chaque page, propositions publiées (`PROPOSITIONS` : la 3 et la 6), rayons (`CATEGORIES`). |
| `outils/contenu.json` | Textes et produits repris du site actuel (rayons, produits, horaires…). |
| `outils/dimensions.json` | Dimensions des images (cadrage des images très verticales). |
| `outils/verifier.py` | Vérifie qu'aucun lien ni ressource locale n'est cassé. |
| `assets/css/base.css` | Mise en page de la proposition retenue (y compris responsive). |
| `assets/css/p3.css` | Thème « Nuit gourmande » : couleurs, polices, héros de l'accueil. |
| `assets/css/p6.css` | **Site actuel** reproduit pour comparaison (fonctions `a_*` de `generer.py`). Feuille autonome : `base.css` n'est pas chargée. |
| `assets/css/switch.css` | Sélecteur « 3 / Actuel » (pastille en bas). |
| `assets/css/choix.css` | Page d'accueil des maquettes (proposition retenue et site actuel). |
| `assets/js/site.js` | Interactions : horaires du jour, menu mobile, en-tête collant, carrousel, « Lire la suite », sélecteur de proposition. |
| `assets/img/`, `assets/fonts/` | Images du site actuel et polices locales. |
| `assets/apercus/` | Vignettes de la page de choix (capture 1440 × 990 de l'accueil, sans la pastille). |
| `proposition-3/*.html`, `proposition-6/*.html`, `index.html` | **Fichiers générés** : ne jamais les modifier à la main. |

## Faire une modification

1. Modifier la source : `outils/generer.py` ou `outils/contenu.json` pour la structure ou le texte,
   `assets/css/*.css` pour l'apparence, `assets/js/site.js` pour les comportements.
   - La mise en page va dans `base.css`, les couleurs, polices et le héros dans `p3.css`.
2. Si `outils/` a changé, régénérer depuis la racine : `python3 outils/generer.py`.
3. Vérifier les liens : `python3 outils/verifier.py`. Il doit afficher 0 lien cassé.
4. Pour un changement visuel, contrôler le rendu :
   - en largeur 1440 px et 390 px (mobile) ;
   - avec Chrome (`$CHROME_PATH`) en headless, par exemple Playwright Python : `pip install playwright`, puis `chromium.launch(executable_path=os.environ["CHROME_PATH"])` ;
   - servir le site avec `python3 -m http.server 8765` depuis la racine ;
   - les images sont en `loading="lazy"` : faire défiler la page avant une capture pleine page.
5. Commit en français sur `main`, puis `git push origin main`.
   - Le propriétaire veut que ce soit en ligne directement, donc pas de branche ni de PR, sauf s'il le demande.
   - Si la session travaille sur une autre branche, fusionner dans `main` puis pousser `main`.
6. Attendre la publication, environ 1 à 2 minutes :
   - vérifier avec `curl -s https://nicownchtr.github.io/rameau-olivier-maquettes/<page> | grep <texte modifié>` ;
   - ou consulter `gh api repos/nicownchtr/rameau-olivier-maquettes/pages/builds/latest`.

   Dans le résumé, préciser qu'il peut falloir recharger la page sans cache.

## À respecter

- Garder le logo (`assets/img/Rameau-Logo.png`, blanc, coloré en CSS via un masque et `--logo`).
- Adresse : **12 rue de Pologne**. « 1972 » est l'année d'ouverture, pas un numéro de rue.
- Le menu dit **« Cadeaux d'entreprise »**, jamais « Cadeaux » seul. Le propriétaire y tient.
- Toutes les pages gardent `<meta name="robots" content="noindex, nofollow">` : ce sont des maquettes.
- Les couleurs passent par les variables CSS du `:root` de chaque `pN.css`. Pas de couleur en dur dans `base.css`.
- Mobile :
  - le menu se ferme avec `visibility: hidden` ;
  - un enfant ne doit jamais repasser en `visibility: visible`, sinon il reste cliquable sous la page (utiliser `inherit`).
- En-tête collant :
  - il ne doit jamais changer de hauteur dans le flux de la page, sinon le contenu saute au défilement ;
  - utiliser `--header-shrink` (top négatif) et des `transform`.
- La proposition 6 reproduit le site actuel : ne pas l'« améliorer », elle doit rester fidèle à rameau-olivier.fr.
