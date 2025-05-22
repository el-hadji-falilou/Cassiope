#!/usr/bin/env python3
import subprocess
import sys
import os

# --- 1) Vérification que minicipher-main.py existe ---
if not os.path.isfile("minicipher-main.py"):
    sys.stderr.write("Erreur : minicipher-main.py introuvable dans le répertoire courant.\n")
    sys.exit(1)

# --- 2) Vos sous-clés en clé 80 bits (hex MSB first) et IV 16 bits ---
KEY_80 = "7e9914dc7c76d6bf5d8e"
IV16   = "0000"

# --- 3) Construction de la commande ---
cmd = [
    sys.executable, "minicipher-main.py",
    "-d",       # mode déchiffrement
    "-b",       # flux binaire
    "-M",       # CBC + padding
    "-k", KEY_80,
    "-i", IV16
]

# --- 4) Lancement du processus, en lui donnant message.xyz sur stdin ---
try:
    with open("message.xyz", "rb") as fin:
        proc = subprocess.run(
            cmd,
            stdin=fin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
except subprocess.CalledProcessError as e:
    sys.stderr.write("Échec de minicipher-main.py :\n")
    sys.stderr.write(e.stderr.decode("utf-8", errors="ignore"))
    sys.exit(1)

# --- 5) Écriture du résultat sur stdout (ou dans un fichier) ---
sys.stdout.buffer.write(proc.stdout)
