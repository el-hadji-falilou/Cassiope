#!/usr/bin/env python

###########################################################
# calcul_probas.py : program to compute the probabilities #
# of the S-Boxes, needed to assess the quality of the     #
# differential paths                                      #
###########################################################

import sys

s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

probas = [[0] * 16 for _ in range(16)]

with open("message.xyz", "rb") as f:
    print(f.read(100))  # Affiche les 100 premiers octets bruts


def compute_probas():
    global probas, s
    # Parcours de toutes les différences d'entrée Δ_in
    for delta_in in range(16):
        # Parcours de toutes les valeurs possibles de x
        for x in range(16):
            # Calcul de la différence de sortie
            delta_out = s[x] ^ s[x ^ delta_in]
            # Incrémentation du comptage
            probas[delta_in][delta_out] += 1



def print_probas():
    # Print the first line
    sys.stdout.write("   |")
    for delta_out in range(16):
        sys.stdout.write(" %x " % delta_out)
    sys.stdout.write("\n")

    sys.stdout.write("-" * (16 * 3 + 4))
    sys.stdout.write("\n")

    for delta_in in range(16):
        sys.stdout.write(" %x |" % delta_in)
        for delta_out in range(16):
            sys.stdout.write("%2d " % probas[delta_in][delta_out])
        sys.stdout.write("\n")
compute_probas()
print_probas()

def find_best_differential_paths():
    """ Trouve et affiche les différences (Δ_in, Δ_out) avec les plus grandes probabilités """
    best_paths = []  # Stocke les meilleurs chemins différentiels sous forme de tuples (Δ_in, Δ_out, probabilité)

    # Parcours de la table des probabilités
    for delta_in in range(16):
        for delta_out in range(16):
            if probas[delta_in][delta_out] > 1:  # On ignore les chemins improbables (0 ou 1)
                best_paths.append((delta_in, delta_out, probas[delta_in][delta_out]))

    # Trier par probabilité décroissante
    best_paths.sort(key=lambda x: x[2], reverse=True)

    # Affichage des résultats
    print("\nMeilleurs chemins différentiels :")
    print("Δ_in | Δ_out | Proba")
    print("----------------------")
    for delta_in, delta_out, prob in best_paths[:10]:  # Afficher les 10 meilleurs
        print(f"  {delta_in:02x}   |  {delta_out:02x}   |   {prob}/16")

# Exécuter l'analyse des chemins les plus probables
find_best_differential_paths()



