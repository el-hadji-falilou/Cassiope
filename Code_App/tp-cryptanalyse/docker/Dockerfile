FROM python:3.9-slim

WORKDIR /code

# Copier les fichiers nécessaires
COPY app/downloads/test-encryption.sh .
COPY app/downloads/test-decryption.sh .
COPY app/downloads/test-identity.sh .

# Installer les dépendances (si nécessaire)
RUN apt-get update && apt-get install -y bash

# Donner les permissions d'exécution aux scripts
RUN chmod +x test-encryption.sh test-decryption.sh test-identity.sh

CMD ["bash"]

# Commande pour lancer l'application Flask
CMD ["python", "app/app.py"]