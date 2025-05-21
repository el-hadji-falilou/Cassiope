##### START_QUESTION_8 #####
s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
# À compléter : inverser la S-box (s_inv)


def find_k5_part1() -> int:
     """
     Trouve les 8 bits de k5 (masque 0x0F0F) en testant :
         1. Toutes les clés candidates 8 bits
         2. Pour chaque paire (C, C') dans pairs-k5_0b00_0606.txt, vérifie si C⊕k5 et C'⊕k5 donnent le Δ attendu après S-box inverse

     Retourne la clé avec le plus de succès
     """
##### END_QUESTION_8 #####



##### START_QUESTION_9 #####
def find_k5_part2() -> int:
     """
     Trouve les 8 bits de k5 (masque 0xF0F0) en testant :
         1. Toutes les clés candidates 8 bits
         2. Pour chaque paire (C, C') dans pairs-k5_000d_a0a0.txt, vérifie si C⊕k5 et C'⊕k5 donnent le Δ attendu après S-box inverse

     Retourne la clé avec le plus de succès
     """
##### END_QUESTION_9 #####



##### START_QUESTION_12 #####

##### END_QUESTION_12 #####



##### START_QUESTION_14 #####

##### END_QUESTION_14 #####



##### START_QUESTION_15 #####

##### END_QUESTION_15 #####
