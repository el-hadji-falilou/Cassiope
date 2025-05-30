# Image légère avec Python, Make et Bash
FROM python:3.10-slim 

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers nécessaires dans le même répertoire
COPY entrypoint.sh               /app/entrypoint.sh
COPY test-decryption.sh          /app/test-decryption.sh
COPY test-decryption.0.txt       /app/test-decryption.0.txt
COPY minicipher-main.py          /app/minicipher-main.py
COPY minicipher.py               /app/minicipher.py
COPY minicipher                  /app/minicipher

# Donner les permissions d'exécution aux scripts
RUN chmod +x /app/entrypoint.sh /app/test-decryption.sh

# Définir le point d'entrée du conteneur
ENTRYPOINT ["/app/entrypoint.sh"]
