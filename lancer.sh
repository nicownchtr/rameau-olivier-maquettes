#!/usr/bin/env bash
# Lance les maquettes sur http://localhost:8080 (Ctrl+C pour arrêter)
cd "$(dirname "$0")"
echo "Maquettes disponibles sur : http://localhost:8080"
python3 -m http.server 8080
