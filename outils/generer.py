"""Génère les propositions de maquettes (HTML statique) à partir de contenu.json.

Usage (depuis la racine du dépôt) : python3 outils/generer.py
Sortie : proposition-3/*.html (proposition retenue) et index.html (redirection) et index.html à la racine du dépôt.
"""
import html
import json
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.dirname(ICI)  # racine du dépôt publié sur GitHub Pages
C = json.load(open(os.path.join(ICI, "contenu.json"), encoding="utf-8"))
DIMS = json.load(open(os.path.join(ICI, "dimensions.json"), encoding="utf-8"))

e = html.escape
IMG = "../assets/img/"

# ---------------------------------------------------------------- propositions
PROPOSITIONS = [
    {"id": 3, "nom": "Nuit gourmande", "css": "p3.css"},
]

# ---------------------------------------------------------------- catégories
CATEGORIES = [
    # (fichier, slug source, nom, accroche, image, groupe)
    ("thes.html", "thes-mariage-freres-a-st-germain-en-laye", "Thés Mariage Frères",
     "Plus de 100 thés en vrac, en boîtes ou en mousselines", "PARIS-MARAIS-V2.jpg", "Thés & cafés"),
    ("cafes.html", "cafes-dexception", "Cafés d'exception",
     "Torréfiés artisanalement par Dasi Frères à Amiens", "FIRENZE-683x1024.webp", "Thés & cafés"),
    ("huiles-olive.html", "nos-huiles-dolive-aop", "Huiles d'olive AOP",
     "Des cuvées françaises et italiennes d'exception", "VILLA-ZOTTOPERA-2-FORMATS-716x1024.jpg", "Huiles & saveurs"),
    ("vinaigres.html", "vinaigres-balsamiques-artisanaux", "Vinaigres balsamiques & artisanaux",
     "De Modène à la Normandie, en passant par Jerez", "COFFRET-3-VELOURS-DE-LABBAYE.jpg", "Huiles & saveurs"),
    ("epices.html", "sels-poivres-epices", "Sels, poivres & épices",
     "120 références Terre Exotique et La Plantation", "POIVRE-DE-KAMPOT-FRAIS-LA-PLANTATION-1024x1024.jpg", "Huiles & saveurs"),
    ("condiments.html", "sauces-condiments", "Sauces & condiments",
     "Moutardes, ail noir, marinades et bouillons", "GAMME-MOUTARDES-V3.webp", "Huiles & saveurs"),
    ("apero.html", "lheure-de-lapero", "L'heure de l'apéro",
     "Tartinables, trésors de la mer et boissons sans alcool", "GAMME-JNPR.jpg", "Plaisirs gourmands"),
    ("truffe-foie-gras.html", "specialites-truffe-foie-gras", "Truffe & foie gras",
     "Spécialités truffées et foie gras de la Maison Barthouil", "FOIE-GRAS-DE-CANARD-ENTIER.jpg", "Plaisirs gourmands"),
    ("douceurs.html", "douceurs-sucrees", "Douceurs sucrées",
     "Confitures, biscuits, chocolats et fruits secs", "GAMME-CONFITURES.jpg", "Plaisirs gourmands"),
]
GROUPES = ["Thés & cafés", "Huiles & saveurs", "Plaisirs gourmands"]

# Titres de produits retravaillés : nom + mention secondaire
TITRES = {
    "Thé vert Marco Polo": ("Marco Polo", "Thé vert"),
    "Thé Matcha Thé vert": ("Matcha", "Thé vert"),
}

HORAIRES = [
    ("Mardi", "9h30 – 13h15 · 14h30 – 19h00"),
    ("Mercredi", "9h30 – 13h00 · 14h30 – 19h00"),
    ("Jeudi", "9h30 – 13h00 · 14h30 – 19h00"),
    ("Vendredi", "9h30 – 13h15 · 14h30 – 19h00"),
    ("Samedi", "9h30 – 13h15 · 14h30 – 19h00"),
    ("Dimanche", "10h00 – 13h00"),
    ("Lundi", "Fermé"),
]

NOUVEAUTES = [
    ("Calendrier de l'Avent Mariage Frères", "MARIAGE-FRERES.jpg"),
    ("Calendrier Oliviers & Co", "OLIVIERS-CO-CALENDAR.jpg"),
    ("Calendrier Le Roy René", "CALENDRIER-AVENT-2026.jpg"),
    ("Calendrier Terre Exotique", "CALENDRIER-TERRE-EXOTIQUE-V3.png"),
    ("Moutardes de Versailles", "MOUTARDE-DE-VERSAILLES.jpg"),
    ("Calendrier Sophie M", "CALENDRIER-AVENT-TASTY-V2.jpg"),
    ("Les bouillons Oumami", "LE-BOUILLON-PHO-EPICURE-2025-1.jpg"),
    ("Foie gras Barthouil", "FOIE-GRAS-DE-CANARD-ENTIER.jpg"),
]

TEMOIGNAGES = [
    ("Le Rameau d'Olivier… plus qu'une épicerie… c'est le cœur gourmand de notre coffee shop, "
     "une histoire de goût partagée entre amis et qui fait pétiller nos plats.", "L. Roch", "Café Noly"),
    ("Un lieu de découverte et de plaisir pour les gourmands et les passionnés de gastronomie.",
     "L. Francony", ""),
    ("Pour le plus grand plaisir de nos hôtes, le Rameau d'Olivier nous a aidés à choisir les 1000 petites "
     "choses qui subliment un plat basique. Notre plateau d'épices et de condiments regorge de curiosités, "
     "au point d'en faire notre signature.", "N. Roselier", "Le Moulin de Tounayne"),
]

COFFRETS = [
    ("Coffret dégustation 3 Velours de l'Abbaye 50 ml", "24,50 €", "COFFRET-3-VELOURS-DE-LABBAYE.jpg"),
    ("Coffret 3 tartinables du Domaine Terra", "29,70 €", "COFFRET-3-TARTINABLES-DOMAINE-TERRA.jpg"),
    ("Sélection « Autour de l'apéro »", "à partir de 34 €", "SELECTION-AUTOUR-DE-LAPERO-V2-1024x932.jpg"),
    ("Coffret 3 balsamiques de Modène médaillés", "49,50 €", "COFFRET-3-MEDAILLES-GIUSEPPE-GIUSTI-1024x1024.webp"),
    ("Sélection « Fraîche et fruitée »", "à partir de 57,30 €", "SELECTION-FRUITEE-V2-1024x923.jpg"),
    ("Sélection « Pause goûter »", "à partir de 75 €", "SELECTION-PAUSE-GOUTER-1-e1757607936353.jpg"),
    ("Sélection « Escapade gourmande »", "à partir de 119 €", "SELECTION-ESCAPADE-GOURMANDE-1024x777.jpg"),
]

ADRESSE = "12 rue de Pologne, 78100 Saint-Germain-en-Laye"
TEL, TEL_LIEN = "01 34 51 56 35", "+33134515635"
MAIL = "contact@rameau-olivier.fr"
MAPS = "https://www.google.com/maps/search/?api=1&query=Le+Rameau+d%27Olivier+12+rue+de+Pologne+Saint-Germain-en-Laye"
FB, IG = "https://www.facebook.com/epiceriefine78", "https://www.instagram.com/lerameaudolivier/"

# ---------------------------------------------------------------- petites aides
ICONES = {
    "fleche": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "gauche": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "horloge": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "colis": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="m3 7.5 9 4.5 9-4.5M12 12v9"/></svg>',
    "cadeau": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="8" width="18" height="4"/><path d="M5 12v9h14v-9M12 8v13M12 8S10.5 3 8 4s0 4 4 4zm0 0s1.5-5 4-4-0 4-4 4z"/></svg>',
    "feuille": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19C5 10 11 5 20 4c-1 9-6 15-15 15z"/><path d="M5 19 14 10"/></svg>',
    "loupe": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/></svg>',
    "coeur": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10A4.5 4.5 0 0 1 12 7.3 4.5 4.5 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/></svg>',
    "bulle": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".6"/></svg>',
}


def ico(nom):
    return f'<span class="ico">{ICONES[nom]}</span>'


def paras(texte, cls=""):
    c = f' class="{cls}"' if cls else ""
    return "".join(f"<p{c}>{e(p)}</p>" for p in texte.split("\n") if p.strip())


def img(nom, alt="", cls="", loading="lazy"):
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{IMG}{nom}" alt="{e(alt)}"{c} loading="{loading}" decoding="async">'


def cadrage(nom):
    """« is-tall » pour les images très verticales (bouteilles détourées) : affichées en entier."""
    w, h = DIMS.get(nom, (1, 1))
    return " is-tall" if w / h < 0.6 else ""


def textes_categorie(slug):
    t = [x for x in C[slug]["textes"] if not (x.isupper() and len(x) < 60)]
    return t[0], (t[1] if len(t) > 1 else "")


def decouper_titre(titre):
    if titre in TITRES:
        return TITRES[titre]
    if " – " in titre:
        nom, reste = titre.split(" – ", 1)
        return nom, reste.replace(" – ", " · ")
    m = re.match(r"^(.*?)\s+(Thé (?:noir|vert|bleu|blanc|rouge).*)$", titre)
    if m:
        return m.group(1), m.group(2)
    return titre, ""


# ---------------------------------------------------------------- gabarit commun
def entete(actif):
    def lien(href, label):
        cur = ' aria-current="page"' if actif == href else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    colonnes = ""
    for g in GROUPES:
        items = "".join(
            f'<li><a href="{f}"{" aria-current=page" if actif == f else ""}>'
            f'<span class="mega-thumb">{img(im)}</span>'
            f'<span><strong>{e(n)}</strong><small>{e(a)}</small></span></a></li>'
            for f, s, n, a, im, gr in CATEGORIES if gr == g)
        colonnes += f'<div class="mega-col"><p class="mega-title">{e(g)}</p><ul>{items}</ul></div>'
    produits_actif = actif == "produits.html" or actif in [c[0] for c in CATEGORIES]
    return f"""
<a class="skip" href="#contenu">Aller au contenu</a>
<div class="topbar">
  <div class="container topbar-inner">
    <span>{ico("pin")}{e(ADRESSE)}</span>
    <span class="topbar-hours" data-today-hours>{ico("horloge")}Du mardi au dimanche</span>
    <a href="tel:{TEL_LIEN}">{ico("tel")}{TEL}</a>
  </div>
</div>
<header class="site-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Le Rameau d'Olivier, retour à l'accueil"><span class="logo"></span><span class="brand-tag">Épicerie fine</span></a>
    <nav class="main-nav" id="menu" aria-label="Menu principal">
      <ul class="nav-list">
        <li class="has-mega">
          <a href="produits.html" class="nav-produits"{' aria-current="page"' if produits_actif else ""}>Nos produits <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></a>
          <div class="mega">
            <div class="container mega-inner">
              {colonnes}
              <a class="mega-feature" href="cadeaux.html">
                {img("SELECTION-ESCAPADE-GOURMANDE-1024x777.jpg")}
                <span class="mega-feature-text"><small>Idées cadeaux</small><strong>Coffrets & sélections gourmandes</strong><em>dès 24,50 € {ICONES["fleche"]}</em></span>
              </a>
            </div>
          </div>
        </li>
        <li>{lien("inspiration-deco.html", "Inspiration déco")}</li>
        <li>{lien("cadeaux.html", "Cadeaux d'entreprise")}</li>
        <li>{lien("notre-histoire.html", "Notre histoire")}</li>
        <li class="nav-mobile-only">{lien("contact.html", "Contact & horaires")}</li>
      </ul>
    </nav>
    <a class="btn btn-header" href="contact.html"{' aria-current="page"' if actif == "contact.html" else ""}>Nous rendre visite</a>
    <button class="burger" type="button" aria-controls="menu" aria-expanded="false" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>
  </div>
</header>
"""


def pied():
    cats = "".join(f'<li><a href="{f}">{e(n)}</a></li>' for f, s, n, a, im, g in CATEGORIES)
    heures = "".join(f'<li data-day="{j}"><span>{j}</span><span>{h}</span></li>' for j, h in HORAIRES)
    return f"""
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <span class="logo"></span>
      <p>Épicerie fine à Saint-Germain-en-Laye depuis 1972. Plus de 1000 références sélectionnées avec soin auprès de près de 50 producteurs.</p>
      <div class="socials">
        <a href="{FB}" aria-label="Facebook">{ICONES["fb"]}</a>
        <a href="{IG}" aria-label="Instagram">{ICONES["ig"]}</a>
      </div>
    </div>
    <div><p class="footer-title">Nos produits</p><ul class="footer-links">{cats}</ul></div>
    <div><p class="footer-title">La maison</p><ul class="footer-links">
      <li><a href="notre-histoire.html">Notre histoire</a></li>
      <li><a href="inspiration-deco.html">Inspiration déco</a></li>
      <li><a href="cadeaux.html">Cadeaux d'entreprise</a></li>
      <li><a href="contact.html">Nous contacter</a></li></ul></div>
    <div><p class="footer-title">Horaires</p><ul class="hours hours-compact">{heures}</ul>
      <p class="footer-addr">{e(ADRESSE)}<br><a href="tel:{TEL_LIEN}">{TEL}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p></div>
  </div>
  <div class="container footer-bottom">
    <span>© Le Rameau d'Olivier</span>
    <span><a href="#">Mentions légales</a> · <a href="#">Politique de confidentialité</a> · <a href="#">Gestion des cookies</a></span>
  </div>
</footer>
"""


def page(prop, fichier, titre, corps, desc=""):
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc or "Le Rameau d'Olivier, épicerie fine à Saint-Germain-en-Laye depuis 1972.")}">
<link rel="icon" href="{IMG}cropped-FAVICON-192x192.png">
<link rel="stylesheet" href="../assets/fonts/fonts.css">
<link rel="stylesheet" href="../assets/css/base.css">
<link rel="stylesheet" href="../assets/css/{prop["css"]}">
<script type="speculationrules">{{"prerender":[{{"where":{{"href_matches":"*.html"}},"eagerness":"moderate"}}]}}</script>
<script src="../assets/js/site.js" defer></script>
</head>
<body class="p{prop["id"]}">
{entete(fichier)}
<main id="contenu">
{corps}
</main>
{pied()}
</body>
</html>
"""


# ---------------------------------------------------------------- blocs réutilisables
def tuile_categorie(c, idx):
    f, s, n, a, im, g = c
    return f"""<a class="cat-tile" href="{f}">
  <span class="cat-media">{img(im, n)}</span>
  <span class="cat-body"><span class="cat-num">{idx:02d}</span><strong>{e(n)}</strong><small>{e(a)}</small><span class="cat-go">{ICONES["fleche"]}</span></span>
</a>"""


def bloc_visite(titre="Venez nous rendre visite"):
    heures = "".join(f'<li data-day="{j}"><span>{j}</span><span>{h}</span></li>' for j, h in HORAIRES)
    return f"""
<section class="visit">
  <div class="container visit-grid">
    <div class="visit-media">{img("FRANK-DEVANT-BOUTIQUE.jpg", "Frank devant la boutique, 12 rue de Pologne")}</div>
    <div class="visit-body reveal">
      <p class="eyebrow">La boutique</p>
      <h2>{titre}</h2>
      <p class="lead">Au cœur de Saint-Germain-en-Laye, à deux pas du marché. On prend le temps de découvrir, de goûter et d'échanger.</p>
      <ul class="visit-facts">
        <li>{ico("pin")}<span>{e(ADRESSE)}</span></li>
        <li>{ico("tel")}<a href="tel:{TEL_LIEN}">{TEL}</a></li>
        <li>{ico("mail")}<a href="mailto:{MAIL}">{MAIL}</a></li>
      </ul>
      <ul class="hours">{heures}</ul>
      <div class="btn-row">
        <a class="btn" href="{MAPS}" target="_blank" rel="noopener">Itinéraire {ICONES["fleche"]}</a>
        <a class="btn btn-ghost" href="contact.html">Nous écrire</a>
      </div>
    </div>
  </div>
</section>"""


def carte_produit(p, i):
    nom, meta = decouper_titre(p["titre"])
    image = p["image"].split("/")[-1]
    return f"""<article class="product reveal" style="--i:{i % 4}">
  <div class="product-media{cadrage(image)}">{img(image, nom)}</div>
  <div class="product-body">
    {f'<p class="product-meta">{e(meta)}</p>' if meta else ''}
    <h3>{e(nom)}</h3>
    <div class="product-desc" data-clamp>{paras(p["texte"])}</div>
    <button type="button" class="more" data-more hidden>Lire la suite</button>
  </div>
</article>"""


# ---------------------------------------------------------------- héros de l'accueil
def hero(prop):
    intro = ("Plus de 1000 références sélectionnées avec soin, souvent issues de circuits artisanaux "
             "ou locaux et dotées d'une histoire. Un lieu où l'on prend le temps de découvrir, de goûter et d'échanger.")
    return f"""
<section class="hero hero-nuit">
  <div class="hero-bg">{img("FRANK-DEVANT-BOUTIQUE.jpg", "", loading="eager")}</div>
  <div class="container hero-content">
    <p class="eyebrow"><span class="rule"></span>Épicerie fine · depuis 1972</p>
    <h1 class="hero-title"><span class="logo" role="img" aria-label="Le Rameau d'Olivier"></span><span class="hero-sub">Le temple <em>des saveurs</em></span></h1>
    <p class="lead">{intro}</p>
    <div class="btn-row">
      <a class="btn" href="produits.html">Découvrir nos produits {ICONES["fleche"]}</a>
      <a class="btn btn-ghost" href="contact.html">Horaires & accès</a>
    </div>
  </div>
  <div class="container hero-foot">
    <ul class="stats">
      <li><strong>1972</strong><span>année d'ouverture</span></li>
      <li><strong>1000+</strong><span>références</span></li>
      <li><strong>50</strong><span>producteurs</span></li>
    </ul>
  </div>
</section>"""


# ---------------------------------------------------------------- pages
def p_accueil(prop):
    texte = C["home"]["textes"][1].split("\n")
    engagements = C["home"]["textes"][3:7]
    icones_eng = ["feuille", "bulle", "loupe", "cadeau"]
    eng = "".join(f'<li>{ico(icones_eng[i])}<span>{e(t)}</span></li>' for i, t in enumerate(engagements))
    tuiles = "".join(tuile_categorie(c, i + 1) for i, c in enumerate(CATEGORIES))
    nouv = "".join(f"""<article class="rail-card">
        <div class="product-media{cadrage(im)}">{img(im, n)}</div>
        <p class="badge">Nouveauté</p><h3>{e(n)}</h3></article>""" for n, im in NOUVEAUTES)
    tem = "".join(f"""<figure class="quote reveal" style="--i:{i}">
        <blockquote><p>{e(q)}</p></blockquote>
        <figcaption><strong>{e(a)}</strong>{f"<span>{e(s)}</span>" if s else ""}</figcaption></figure>"""
                  for i, (q, a, s) in enumerate(TEMOIGNAGES))
    corps = f"""
{hero(prop)}

<section class="section univers">
  <div class="container">
    <div class="section-head reveal">
      <div><p class="eyebrow">Nos univers</p><h2>Neuf rayons à explorer</h2></div>
      <a class="link-arrow" href="produits.html">Tous nos produits {ICONES["fleche"]}</a>
    </div>
    <div class="cat-grid">{tuiles}</div>
  </div>
</section>

<section class="section nouveautes">
  <div class="container">
    <div class="section-head reveal">
      <div><p class="eyebrow">En ce moment</p><h2>Nos nouveautés</h2></div>
      <div class="rail-nav"><button type="button" data-rail-prev aria-label="Précédent">{ICONES["gauche"]}</button><button type="button" data-rail-next aria-label="Suivant">{ICONES["fleche"]}</button></div>
    </div>
  </div>
  <div class="rail" data-rail>{nouv}</div>
</section>

<section class="section about">
  <div class="container about-grid">
    <div class="about-media reveal">
      {img("FRANK-NOTRE-HISTOIRE-V2-768x1024.jpg", "Frank, l'épicier du Rameau d'Olivier")}
    </div>
    <div class="about-body reveal">
      <p class="eyebrow">L'épicerie fine</p>
      <h2>Chaque référence a une histoire</h2>
      <p class="lead">{e(texte[0])}</p>
      {paras(chr(10).join(texte[1:]))}
      <h3 class="small-title">Nos engagements</h3>
      <ul class="engagements">{eng}</ul>
      <a class="link-arrow" href="notre-histoire.html">Notre histoire {ICONES["fleche"]}</a>
    </div>
  </div>
</section>

<section class="section temoignages">
  <div class="container">
    <div class="section-head center reveal"><div><p class="eyebrow">Ils nous font confiance</p><h2>Ce qu'en disent nos partenaires</h2></div></div>
    <div class="quotes">{tem}</div>
  </div>
</section>

<section class="section offrir">
  <div class="container offrir-grid">
    <div class="offrir-media reveal">{img("COVER-SELECTION-NOEL-2025-sans-adresse.jpg", "Sélection de Noël")}</div>
    <div class="offrir-body reveal">
      <p class="eyebrow">Le plaisir d'offrir</p>
      <h2>Des cadeaux gourmands, ici ou à distance</h2>
      <div class="offrir-cards">
        <div class="mini-card">{ico("colis")}<h3>Envoi partout en France</h3><p>Vous souhaitez offrir un cadeau gourmand à ceux que vous aimez mais qui se trouvent à distance ? Nous nous chargeons de l'envoi au tarif Colissimo en vigueur.</p></div>
        <div class="mini-card">{ico("cadeau")}<h3>Cadeaux d'entreprise</h3><p>Pour vos clients ou collaborateurs, nous composons des sélections de cadeaux sur mesure.</p></div>
      </div>
      <div class="btn-row"><a class="btn" href="cadeaux.html">Voir les coffrets {ICONES["fleche"]}</a><a class="btn btn-ghost" href="contact.html">Nous contacter</a></div>
    </div>
  </div>
</section>
{bloc_visite()}
"""
    return "Le Rameau d'Olivier · Épicerie fine à Saint-Germain-en-Laye", corps


def fil(*items):
    out = []
    for lab, href in items:
        out.append(f'<a href="{href}">{e(lab)}</a>' if href else f'<span aria-current="page">{e(lab)}</span>')
    return '<nav class="crumbs" aria-label="Fil d\'Ariane">' + '<span class="sep">/</span>'.join(out) + "</nav>"


def chips(actif):
    return '<nav class="chips" aria-label="Rayons"><div class="container chips-inner">' + "".join(
        f'<a href="{f}"{" aria-current=page" if f == actif else ""}>{e(n)}</a>'
        for f, s, n, a, im, g in CATEGORIES) + "</div></nav>"


def p_categorie(prop, cat, idx):
    f, slug, nom, accroche, image, groupe = cat
    intro, outro = textes_categorie(slug)
    produits = C[slug]["produits"]
    cartes = "".join(carte_produit(p, i) for i, p in enumerate(produits))
    prev = CATEGORIES[idx - 1]
    nxt = CATEGORIES[(idx + 1) % len(CATEGORIES)]
    corps = f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div class="page-hero-text">
      {fil(("Accueil", "index.html"), ("Nos produits", "produits.html"), (nom, None))}
      <p class="eyebrow">{e(groupe)}</p>
      <h1>{e(nom)}</h1>
      {paras(intro, "lead")}
    </div>
    <div class="page-hero-media">{img(image, nom, loading="eager")}</div>
  </div>
</section>
{chips(f)}
<section class="section products-section">
  <div class="container">
    <p class="count">Une sélection de {len(produits)} produits parmi nos références en boutique</p>
    <div class="products">{cartes}</div>
    {f'<aside class="note reveal">{ico("feuille")}<div>{paras(outro)}</div></aside>' if outro else ""}
  </div>
</section>
<nav class="pager container" aria-label="Rayons voisins">
  <a href="{prev[0]}" class="pager-prev"><small>{ICONES["gauche"]} Rayon précédent</small><strong>{e(prev[2])}</strong></a>
  <a href="{nxt[0]}" class="pager-next"><small>Rayon suivant {ICONES["fleche"]}</small><strong>{e(nxt[2])}</strong></a>
</nav>
"""
    return f"{nom} · Le Rameau d'Olivier", corps


def p_produits(prop):
    blocs = ""
    n = 0
    for g in GROUPES:
        tuiles, k = "", 0
        for c in CATEGORIES:
            if c[5] == g:
                n += 1
                k += 1
                tuiles += tuile_categorie(c, n)
        blocs += f'<div class="group reveal"><h2 class="group-title">{e(g)}</h2><div class="cat-grid" style="--cols:{k}">{tuiles}</div></div>'
    corps = f"""
<section class="page-hero page-hero-simple">
  <div class="container">
    {fil(("Accueil", "index.html"), ("Nos produits", None))}
    <p class="eyebrow">Plus de 1000 références en boutique</p>
    <h1>Nos produits</h1>
    <p class="lead">Huiles d'olive et vinaigres d'exception, épices du monde entier, condiments, spécialités régionales artisanales et bien entendu des thés prestigieux ou des cafés pure origine.</p>
  </div>
</section>
<section class="section products-overview"><div class="container">{blocs}</div></section>
<section class="section cta-band"><div class="container"><div class="cta-inner reveal">
  <div><h2>Vous ne trouvez pas ce que vous cherchez ?</h2><p>Le site ne présente qu'une partie de nos références. Passez nous voir ou appelez-nous : nous vous conseillerons avec plaisir.</p></div>
  <div class="btn-row"><a class="btn" href="contact.html">Nous contacter {ICONES["fleche"]}</a><a class="btn btn-ghost" href="tel:{TEL_LIEN}">{TEL}</a></div>
</div></div></section>
"""
    return "Nos produits · Le Rameau d'Olivier", corps


def p_deco(prop):
    slug = "inspiration-deco"
    intro, outro = textes_categorie(slug)
    cartes = "".join(carte_produit(p, i) for i, p in enumerate(C[slug]["produits"]))
    corps = f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div class="page-hero-text">
      {fil(("Accueil", "index.html"), ("Inspiration déco", None))}
      <p class="eyebrow">Art de la table japonais & bougies</p>
      <h1>Inspiration déco</h1>
      {paras(intro, "lead")}
    </div>
    <div class="page-hero-media">{img("BOL-SAKURA-AVEC-CUILLER-1024x683.jpg", "Bols Sakura", loading="eager")}</div>
  </div>
</section>
<section class="section products-section"><div class="container">
  <div class="products">{cartes}</div>
  <aside class="note reveal">{ico("feuille")}<div>{paras(outro)}</div></aside>
</div></section>
"""
    return "Inspiration déco · Le Rameau d'Olivier", corps


def p_cadeaux(prop):
    intro = C["cadeaux-dentreprise"]["textes"][0]
    dispo = C["cadeaux-dentreprise"]["textes"][1]
    cartes = "".join(f"""<article class="product gift reveal" style="--i:{i % 4}">
      <div class="product-media">{img(im, n)}</div>
      <div class="product-body"><h3>{e(n)}</h3><p class="price">{e(p)}</p></div></article>"""
                     for i, (n, p, im) in enumerate(COFFRETS))
    corps = f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div class="page-hero-text">
      {fil(("Accueil", "index.html"), ("Cadeaux d'entreprise", None))}
      <p class="eyebrow">Particuliers & entreprises</p>
      <h1>Le plaisir d'offrir</h1>
      {paras(intro, "lead")}
      <div class="btn-row"><a class="btn" href="#coffrets">Voir les coffrets {ICONES["fleche"]}</a><a class="btn btn-ghost" href="contact.html">Demander un devis</a></div>
    </div>
    <div class="page-hero-media">{img("SELECTION-PAUSE-GOUTER-1-e1757607936353.jpg", "Sélection Pause goûter", loading="eager")}</div>
  </div>
</section>
<section class="section services">
  <div class="container services-grid">
    <div class="mini-card reveal">{ico("cadeau")}<h3>Cadeaux d'entreprise sur mesure</h3><p>Récompenser des collaborateurs, fidéliser votre clientèle : nous composons avec vous des sélections à votre image, pour tous les budgets.</p></div>
    <div class="mini-card reveal">{ico("colis")}<h3>Envoi à distance</h3><p>Vos proches sont loin ? Nous nous chargeons de l'envoi de votre cadeau gourmand au tarif Colissimo en vigueur.</p></div>
    <div class="mini-card reveal">{ico("coeur")}<h3>Une touche personnelle</h3><p>Nous sommes là pour vous conseiller et vous guider dans votre sélection, selon les goûts de chacun.</p></div>
  </div>
</section>
<section class="section products-section" id="coffrets"><div class="container">
  <div class="section-head reveal"><div><p class="eyebrow">Suggestions</p><h2>Coffrets & sélections</h2></div></div>
  <div class="products">{cartes}</div>
  <p class="fineprint">{e(dispo)}</p>
</div></section>
<section class="section noel"><div class="container noel-grid reveal">
  <div class="noel-media">{img("COVER-SELECTION-NOEL-2025-sans-adresse.jpg", "Sélection de Noël")}</div>
  <div><p class="eyebrow">Fêtes de fin d'année</p><h2>Découvrez notre sélection de Noël</h2><p>Calendriers de l'Avent, coffrets, foie gras et douceurs : toutes nos idées pour les fêtes, à feuilleter en ligne.</p>
  <a class="btn" href="#">Feuilleter la sélection {ICONES["fleche"]}</a></div>
</div></section>
"""
    return "Cadeaux d'entreprise · Le Rameau d'Olivier", corps


def p_histoire(prop):
    t = C["notre-histoire"]["textes"]
    p2004 = t[2].split("\n")
    eng = "".join(f'<li>{ico(i)}<span>{e(x)}</span></li>' for i, x in zip(["coeur", "feuille", "bulle"], t[4:7]))
    corps = f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div class="page-hero-text">
      {fil(("Accueil", "index.html"), ("Notre histoire", None))}
      <p class="eyebrow">Qui sommes-nous ?</p>
      <h1>Plus de 50 ans rue de Pologne</h1>
      <p class="lead">{e(p2004[1])}</p>
    </div>
    <div class="page-hero-media portrait">{img("FRANK-NOTRE-HISTOIRE-V2-768x1024.jpg", "Frank, épicier du Rameau d'Olivier", loading="eager")}</div>
  </div>
</section>
<section class="section timeline-section"><div class="container">
  <ol class="timeline">
    <li class="reveal"><span class="year">1972</span><div><h2>L'ouverture</h2><p>{e(t[1])}</p></div></li>
    <li class="reveal"><span class="year">2004</span><div><h2>Changement de décor</h2><p>{e(p2004[0].replace("En 2004 : changement de décor ! ", ""))}</p></div></li>
    <li class="reveal"><span class="year year-long">Aujourd'hui</span><div><h2>Toujours la même envie</h2><p>{e(t[3])}</p><ul class="engagements">{eng}</ul></div></li>
  </ol>
</div></section>
<section class="section social-band"><div class="container"><div class="cta-inner reveal">
  <div><h2>Suivez notre actualité</h2><p>Arrivages, nouveautés, coulisses de la boutique : retrouvez-nous sur les réseaux.</p></div>
  <div class="btn-row"><a class="btn" href="{IG}" target="_blank" rel="noopener">{ICONES["ig"]} Instagram</a><a class="btn btn-ghost" href="{FB}" target="_blank" rel="noopener">{ICONES["fb"]} Facebook</a></div>
</div></div></section>
{bloc_visite("Passez nous voir")}
"""
    return "Notre histoire · Le Rameau d'Olivier", corps


def p_contact(prop):
    heures = "".join(f'<li data-day="{j}"><span>{j}</span><span>{h}</span></li>' for j, h in HORAIRES)
    corps = f"""
<section class="page-hero page-hero-simple">
  <div class="container">
    {fil(("Accueil", "index.html"), ("Contact", None))}
    <p class="eyebrow">Une question ou une suggestion ?</p>
    <h1>Nous contacter</h1>
    <p class="lead">Une recherche de produit, une commande de cadeaux, un conseil : écrivez-nous ou passez directement en boutique.</p>
  </div>
</section>
<section class="section contact-section"><div class="container contact-grid">
  <form class="contact-form reveal" data-form>
    <div class="field-row">
      <label><span>Nom</span><input type="text" name="nom" autocomplete="name" required></label>
      <label><span>Téléphone <small>(facultatif)</small></span><input type="tel" name="tel" autocomplete="tel"></label>
    </div>
    <label><span>E-mail</span><input type="email" name="email" autocomplete="email" required></label>
    <label><span>Objet</span>
      <select name="objet"><option>Renseignement produit</option><option>Cadeaux d'entreprise</option><option>Envoi d'un colis cadeau</option><option>Autre</option></select>
    </label>
    <label><span>Message</span><textarea name="message" rows="6" required></textarea></label>
    <button class="btn" type="submit">Envoyer {ICONES["fleche"]}</button>
    <p class="form-ok" hidden>Merci ! (Maquette : le message n'est pas réellement envoyé.)</p>
  </form>
  <aside class="contact-card reveal">
    <span class="logo"></span>
    <ul class="visit-facts">
      <li>{ico("pin")}<span>{e(ADRESSE)}</span></li>
      <li>{ico("tel")}<a href="tel:{TEL_LIEN}">{TEL}</a></li>
      <li>{ico("mail")}<a href="mailto:{MAIL}">{MAIL}</a></li>
    </ul>
    <h2 class="small-title">Horaires</h2>
    <ul class="hours">{heures}</ul>
    <div class="btn-row"><a class="btn" href="{MAPS}" target="_blank" rel="noopener">Itinéraire {ICONES["fleche"]}</a></div>
    <div class="socials"><a href="{FB}" aria-label="Facebook">{ICONES["fb"]}</a><a href="{IG}" aria-label="Instagram">{ICONES["ig"]}</a></div>
  </aside>
</div></section>
<section class="contact-photo">{img("FRANK-DEVANT-BOUTIQUE.jpg", "La façade de la boutique")}</section>
"""
    return "Contact · Le Rameau d'Olivier", corps


# ---------------------------------------------------------------- racine du site
def index_racine():
    """La racine renvoie directement vers l'accueil de la maquette retenue."""
    return """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url=proposition-3/index.html">
<title>Le Rameau d'Olivier · maquette</title>
<link rel="icon" href="assets/img/cropped-FAVICON-192x192.png">
</head><body><p><a href="proposition-3/index.html">Ouvrir la maquette</a></p></body></html>
"""


# ---------------------------------------------------------------- génération
def ecrire(chemin, contenu):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)


def main():
    n = 0
    for prop in PROPOSITIONS:
        dossier = os.path.join(SORTIE, f"proposition-{prop['id']}")
        pages = {
            "index.html": p_accueil(prop),
            "produits.html": p_produits(prop),
            "inspiration-deco.html": p_deco(prop),
            "cadeaux.html": p_cadeaux(prop),
            "notre-histoire.html": p_histoire(prop),
            "contact.html": p_contact(prop),
        }
        for i, cat in enumerate(CATEGORIES):
            pages[cat[0]] = p_categorie(prop, cat, i)
        for fichier, (titre, corps) in pages.items():
            ecrire(os.path.join(dossier, fichier), page(prop, fichier, titre, corps))
            n += 1
    ecrire(os.path.join(SORTIE, "index.html"), index_racine())
    print(f"{n} pages générées dans {SORTIE}")


if __name__ == "__main__":
    main()
