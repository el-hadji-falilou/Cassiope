#!/usr/bin/env python3

###########################################################
# compute-proba.py : computes probabilities for S-Box use #
###########################################################

import json


##### START_QUESTION_4 #####
global probas, s

# S-Box
s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

# Inverse de la S-Box
s_inv = [0] * 16

# probas[i][j] est le nombre de fois qu'on a δout=j sachant que δin=i
probas = [[0 for _ in range(16)] for _ in range(16)]

# On calcule le tableau des probas
def compute_probas():
    # Parcours de toutes les différences d'entrée Δ_in
    for delta_in in range(16):
        # Parcours de toutes les valeurs possibles de x
        for x in range(16):
            # Calcul de la différence de sortie
            delta_out = s[x] ^ s[x ^ delta_in]
            # Incrémentation du comptage
            probas[delta_in][delta_out] += 1
##### END_QUESTION_4 #####


def print_probas():
    print(json.dumps(probas))

if __name__ == "__main__":
    compute_probas()
    print_probas()
