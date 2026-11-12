# Notes de projet — refonte rameau-olivier.fr

Ce fichier est la **mémoire partagée** du projet. Il est synchronisé par git entre les sessions locales et les sessions
cloud (téléphone). Toute décision, toute exigence nouvelle et tout changement d'état se notent ici, dans le même
commit que la modification qui va avec.

## État actuel

- Les 6 propositions sont en ligne. On attend que le patron en choisisse une.
  - 1 Arcades, 2 Lin & caramel, 3 Nuit gourmande, 4 Arcades de nuit, 5 Comptoir, 6 Étiquettes.
- La suite attend aussi :
  - l'archive du site WordPress (Duplicator, ou FTP + dump SQL) ;
  - la vérification que l'offre Ikoula permet un sous-domaine et une deuxième base de données, pour la préproduction.
- Le thème WordPress n'est pas commencé.

## Exigences du propriétaire

- Menu : « **Cadeaux d'entreprise** », jamais « Cadeaux » seul. Le propriétaire y tient.
- Adresse : 12 rue de Pologne. 1972 est l'année d'ouverture.
- Garder le logo.
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

- 2026-11-12 — Synchroniser la mémoire entre le local et le cloud → ce fichier, chargé par `CLAUDE.md`. En local, faire `git pull` en début de session.
- 2026-11-06 — (session cloud) Proposition 6 « Étiquettes » : vert olive, store banne, étiquettes, polices Bricolage Grotesque + Instrument Serif, héros en tirages photo avec tampon tournant et bandeau défilant des rayons.
- 2026-11-06 — Piloter les maquettes depuis le téléphone → générateur et `CLAUDE.md` ajoutés au dépôt, push direct sur `main`.
- 2026-11-06 — L'en-tête collant donnait un à-coup au premier cran de défilement → il garde sa hauteur dans la page (`--header-shrink`).
- 2026-11-05 — Menu mobile fermé mais encore cliquable → le sous-menu hérite de la visibilité du menu.
- 2026-11-05 — Deux propositions de plus : la 4 (mise en page de la 1, couleurs de la 3) et la 5 (Comptoir).
- 2026-11-04 — Corrections : adresse, chevauchement de « Aujourd'hui » dans la frise, photo du patron recadrée, « Cadeaux d'entreprise ». Mise en ligne sur GitHub Pages.
