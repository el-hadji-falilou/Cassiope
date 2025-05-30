# Image légère avec Python, Make et Bash
FROM python:3.10-slim 

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers nécessaires dans le même répertoire
COPY entrypoint.sh           /app/entrypoint.sh
COPY test_k5_1.sh            /app/test_k5_1.sh
COPY find_key.py             /app/find_key.py
COPY pairs_k5_0b00_0606.txt  /app/pairs_k5_0b00_0606.txt

# Donner les permissions d'exécution aux scripts
RUN chmod +x /app/test_k5_1.sh /app/entrypoint.sh

# Définir le point d'entrée du conteneur
ENTRYPOINT ["/app/entrypoint.sh"]
