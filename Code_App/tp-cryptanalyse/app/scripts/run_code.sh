# run_code.sh
#!/bin/bash

# Exécuter le code de l'étudiant
python3 minicipher.py > output.txt

# Vérifier si output.txt existe
if [ ! -f "output.txt" ]; then
    echo "Erreur : output.txt n'a pas été créé."
    exit 1
fi

# Comparer la sortie avec les fichiers de référence
python3 validate_code.py