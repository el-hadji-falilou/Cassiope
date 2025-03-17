# Image légère avec Python, Make et Bash
FROM python:3.10-slim 

# Installer Make (nécessaire pour la compilation)
RUN apt-get update && apt-get install -y make

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers nécessaires dans le même répertoire
COPY entrypoint.sh /app/entrypoint.sh
COPY test-encryption.sh /app/test-encryption.sh
COPY test-encryption.0.txt /app/test-encryption.0.txt
COPY minicipher-main.py /app/minicipher-main.py
COPY minicipher.py /app/minicipher.py
COPY Makefile /app/Makefile

# Donner les permissions d'exécution aux scripts
RUN chmod +x /app/entrypoint.sh /app/test-encryption.sh

# Définir le point d'entrée du conteneur
ENTRYPOINT ["/app/entrypoint.sh"]