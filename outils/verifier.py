"""Vérifie les maquettes générées : liens et ressources locales introuvables.

Usage (depuis la racine du dépôt) : python3 outils/verifier.py
Code de sortie 1 s'il y a des liens cassés.
"""
import os
import re
import sys
from urllib.parse import unquote, urlparse

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTR = re.compile(r'(?:href|src|poster)="([^"]+)"|url\((["\']?)([^)"\']+)\2\)')


def cibles(texte):
    for m in ATTR.finditer(texte):
        yield m.group(1) or m.group(3)


def externe(lien):
    u = urlparse(lien)
    return u.scheme in ("http", "https", "mailto", "tel", "data", "javascript") or lien.startswith(("#", "//"))


def main():
    pages, casses = 0, []
    for dossier, sous, fichiers in os.walk(RACINE):
        sous[:] = [d for d in sous if not d.startswith(".") and d != "outils"]
        for nom in fichiers:
            if not nom.endswith((".html", ".css")):
                continue
            chemin = os.path.join(dossier, nom)
            pages += nom.endswith(".html")
            texte = open(chemin, encoding="utf-8").read()
            for lien in cibles(texte):
                if externe(lien):
                    continue
                cible = os.path.normpath(os.path.join(dossier, unquote(urlparse(lien).path)))
                if not os.path.exists(cible):
                    casses.append(f"{os.path.relpath(chemin, RACINE)} -> {lien}")
    for c in sorted(set(casses)):
        print("CASSÉ :", c)
    print(f"{pages} pages HTML vérifiées, {len(set(casses))} lien(s) cassé(s).")
    sys.exit(1 if casses else 0)


if __name__ == "__main__":
    main()
