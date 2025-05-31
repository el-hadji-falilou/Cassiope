# Image légère avec Python, Make et Bash
FROM python:3.10-slim 

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers nécessaires dans le même répertoire
COPY entrypoint.sh            /app/entrypoint.sh
COPY test_k1_k2.sh            /app/test_k1_k2.sh
COPY find_key.py              /app/find_key.py
COPY plaintext_ciphertext.txt /app/plaintext_ciphertext.txt
COPY pairs_k2_bbbb.txt        /app/pairs_k2_bbbb.txt
COPY pairs_k3_0220.txt        /app/pairs_k3_0220.txt
COPY pairs_k3_1010.txt        /app/pairs_k3_1010.txt
COPY pairs_k4_0005.txt        /app/pairs_k4_0005.txt
COPY pairs_k4_0040.txt        /app/pairs_k4_0040.txt
COPY pairs_k5_000d_a0a0.txt   /app/pairs_k5_000d_a0a0.txt
COPY pairs_k5_0b00_0606.txt   /app/pairs_k5_0b00_0606.txt

# Donner les permissions d'exécution aux scripts
RUN chmod +x /app/test_k1_k2.sh /app/entrypoint.sh

# Définir le point d'entrée du conteneur
ENTRYPOINT ["/app/entrypoint.sh"]
