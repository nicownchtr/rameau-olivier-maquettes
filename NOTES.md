# Notes de projet — refonte rameau-olivier.fr

Ce fichier est la **mémoire partagée** du projet. Il est synchronisé par git entre les sessions locales et les sessions
cloud (téléphone). Toute décision, toute exigence nouvelle et tout changement d'état se notent ici, dans le même
commit que la modification qui va avec.

## État actuel

- **Le patron a choisi la proposition 3 « Nuit gourmande »** (2026-11-16). C'est la base du thème WordPress.
  - Les propositions 1, 2, 4 et 5 sont supprimées (récupérables dans l'historique git, commit 2509239). L'ancienne 6 « Étiquettes » aussi (commit 2e834f1).
  - La reproduction du site actuel (6) est supprimée aussi (commit 9aaf570 pour la récupérer). La racine du site redirige vers la 3.
  - Accueil : le logo remplace le titre, « Le temple des saveurs » devient un sous-titre ; la photo de la boutique est à droite (au-dessus du texte sur mobile) pour que le texte ne cache jamais le patron.
- La suite attend aussi :
  - l'archive du site WordPress (Duplicator, ou FTP + dump SQL) ;
  - la vérification que l'offre Ikoula permet un sous-domaine et une deuxième base de données, pour la préproduction.
- Le thème WordPress n'est pas commencé : on le lance sur la base de la 3 (question préalable sur les modèles créés depuis l'interface, voir Journal).

## Exigences du propriétaire

- Menu : « **Cadeaux d'entreprise** », jamais « Cadeaux » seul. Le propriétaire y tient.
- Adresse : 12 rue de Pologne. 1972 est l'année d'ouverture.
- Garder le logo. Sur l'accueil, le logo sert de titre, avec « Le temple des saveurs » en sous-titre.
- Le texte de l'accueil ne doit pas recouvrir le patron sur la photo.
- **Tout doit être personnalisable depuis l'interface WordPress** : ajouter, modifier, supprimer des éléments sans code.
- Éviter le côté « vieillot » du site actuel : gros blocs carrés de couleur, mises en page basiques. La navigation doit être fluide.
- Vérifier chaque changement visuel sur ordinateur (1440 px) et sur mobile (390 px).
- Reproduire un bug avant de le corriger.
- Les bugs d'affichage des maquettes valent la peine d'être corrigés tout de suite : les styles et scripts seront repris dans le thème WordPress.

## Plan pour le thème WordPress (validé)

- **Copie locale :** WordPress dans Docker, à partir de l'archive.
- **Thème « blocs » (FSE)**, sans dépendre d'Elementor. Elementor peut rester installé pendant la transition.
  - Couleurs et polices dans `theme.json`.
  - Des compositions prêtes à l'emploi, pour que l'administrateur modifie la mise en page lui-même. Il connaît Elementor et n'a ni Docker ni git.
- **Produits :** type de contenu « Produits » avec une taxonomie « Rayons » (nom, photo, description, mention, case « Nouveauté »).
  - Import automatique des produits existants depuis `outils/contenu.json`.
- **Horaires et coordonnées :** une page de réglages unique. Elle alimente le bandeau du haut, le pied de page, la page contact et la pastille « ouvert aujourd'hui ».
- **Modifications par Claude :** compte WordPress dédié aux droits limités, avec mot de passe d'application, via l'API REST ou un adaptateur MCP.
  - Les brouillons de pages publiées passent par *Yoast Duplicate Post* (« Réécrire et republier ») : l'administrateur prévisualise puis republie.
- **Préproduction** protégée par mot de passe pour les changements de design global.
- **Code du thème sur GitHub**, déploiement du thème seul vers Ikoula. Le contenu se modifie directement en production.

## Journal

Une ligne par demande, la plus récente en haut : `AAAA-MM-JJ — demande → ce qui a été fait / décidé`.

- 2026-11-16 — Supprimer la 6, attaquer le thème sur la base de la 3 ; peut-on créer des modèles d'éléments depuis l'interface ? → 6 supprimée (avec sélecteur, page de choix, polices). Réponse : oui pour tout ce qui est assemblage de blocs (compositions, modèles de page, en-tête/pied, styles globaux) ; du code seulement pour un nouveau comportement ou une nouvelle structure de données.
- 2026-11-16 — Le patron choisit la 3 ; logo à la place du titre de l'accueil, texte qui ne cache plus le patron, suppression des autres maquettes → logo + sous-titre « Le temple des saveurs », photo du héros à droite (au-dessus sur mobile), propositions 1, 2, 4, 5 retirées avec leurs CSS, polices et aperçus. La 6 (site actuel) est gardée pour comparer.
- 2026-11-12 — Remplacer la maquette 6 par le site actuel → proposition 6 = reproduction de rameau-olivier.fr (mêmes pages, textes, couleurs, polices Forum/Merriweather/Open Sans/Sora, menu déroulant, tiroir). « Étiquettes » retirée. Sélecteur déplacé dans `switch.css`.
- 2026-11-12 — Synchroniser la mémoire entre le local et le cloud → ce fichier, chargé par `CLAUDE.md`. En local, faire `git pull` en début de session.
- 2026-11-06 — (session cloud) Proposition 6 « Étiquettes » : vert olive, store banne, étiquettes, polices Bricolage Grotesque + Instrument Serif, héros en tirages photo avec tampon tournant et bandeau défilant des rayons.
- 2026-11-06 — Piloter les maquettes depuis le téléphone → générateur et `CLAUDE.md` ajoutés au dépôt, push direct sur `main`.
- 2026-11-06 — L'en-tête collant donnait un à-coup au premier cran de défilement → il garde sa hauteur dans la page (`--header-shrink`).
- 2026-11-05 — Menu mobile fermé mais encore cliquable → le sous-menu hérite de la visibilité du menu.
- 2026-11-05 — Deux propositions de plus : la 4 (mise en page de la 1, couleurs de la 3) et la 5 (Comptoir).
- 2026-11-04 — Corrections : adresse, chevauchement de « Aujourd'hui » dans la frise, photo du patron recadrée, « Cadeaux d'entreprise ». Mise en ligne sur GitHub Pages.
