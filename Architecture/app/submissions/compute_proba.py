#!/usr/bin/env python3

###########################################################
# compute-proba.py : computes probabilities for S-Box use #
###########################################################

import json


# Variables globales
probas = [[0 for _ in range(16)] for _ in range(16)]


##### START_QUESTION_4 #####
# S-Box Definition
s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

# On inverse la S-Box
s_inv = [0] * 16
# À compléter : inverser la S-box (s_inv)


# probas doit etre un tableau de tableau, probas[i][j] étant le nombre de fois qu'on a δout=j sachant que δin=i
probas = [[0 for _ in range(16)] for _ in range(16)]


# On calcule le tableau des probas
def compute_probas():
     global probas, s
     for delta_in in range(16):
        for x in range(16):
            x_prime = x ^ delta_in
            y = s[x]
            y_prime = s[x_prime]
            delta_out = y ^ y_prime
            probas[delta_in][delta_out] += 1
##### END_QUESTION_4 #####


def print_probas():
    print(json.dumps(probas))

if __name__ == "__main__":
    compute_probas()
    print_probas()
