#!/bin/bash

set -e  # Stopper l'exécution en cas d'erreur critique

# Fichier de code de l'élève
CODE_FILE="/app/minicipher.py"
EXECUTABLE_FILE="/app/minicipher"

# Vérifier si le fichier Python soumis existe
if [ ! -f "$CODE_FILE" ]; then
    echo "Aucun fichier minicipher.py trouvé. Assurez-vous de monter le fichier correctement."
    exit 1
fi

# Exécuter la commande Make pour compiler l'exécutable
make python

# Vérifier si l'exécutable a été créé
if [ ! -f "$EXECUTABLE_FILE" ]; then
    echo "L'exécutable minicipher n'a pas été créé. Vérifiez la compilation."
    exit 1
fi

# Exécuter le script de test avec l'argument `0` et affiche la sortie
bash test-encryption.sh 0