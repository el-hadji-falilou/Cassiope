#!/usr/bin/env python3

# Définition de la S-Box et de son inverse

s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
s_inv = [0] * 16  # Initialisation de l'inverse de la S-Box

# Remplissage de l'inverse de la S-Box
for i in range(16):
    s_inv[s[i]] = i


def read_cipher_pairs(filename):
    """ Lit les paires (C, C') depuis un fichier et retourne une liste de tuples (C, C') """
    pairs = []
    with open(filename, "r") as f:
        for line in f:
            c, c_prime = line.strip().split(', ')
            pairs.append((int(c, 16), int(c_prime, 16)))  # Conversion hex -> int
    return pairs


def recover_k4_using_mask(pairs, expected_delta, mask):
    """ Récupère 8 bits de K4 en utilisant un masque donné """
    scores = [0] * 65536  # 65536 possibilités pour les 16 bits de K4

    for k4 in range(65536):  # Tester toutes les valeurs possibles de K4 (16 bits)
        if k4 & ~mask != 0:  # On ignore les K4 qui ne respectent pas le masque
            continue
        score = 0
        for C, C_prime in pairs:

            # Annuler la dernière sous-clé K4
            T = C ^ k4
            T_prime = C_prime ^ k4

            # Appliquer la S-Box inversée
            U = (s_inv[(T >> 12) & 0xF] << 12) | (s_inv[(T >> 8) & 0xF] << 8) | \
                (s_inv[(T >> 4) & 0xF] << 4) | (s_inv[T & 0xF])

            U_prime = (s_inv[(T_prime >> 12) & 0xF] << 12) | (s_inv[(T_prime >> 8) & 0xF] << 8) | \
                      (s_inv[(T_prime >> 4) & 0xF] << 4) | (s_inv[T_prime & 0xF])

            # Vérifier si la différence obtenue correspond à expected_delta
            if (U ^ U_prime) & mask == expected_delta:
                score += 1

        scores[k4] = score  # Sauvegarder le score pour cette clé

    best_k4 = max(range(65536), key=lambda k: scores[k])  # Trouver la meilleure clé K4
    print(f"Meilleure estimation pour K4 avec masque {mask:04x}: {best_k4:04x} (score = {scores[best_k4]})")
    return best_k4


# Chargement des paires de chiffrés pour K4
pairs_k4_0606 = read_cipher_pairs("../crypto-material/pairs-k4_delta_in_0040.txt")
pairs_k4_a0a0 = read_cipher_pairs("../crypto-material/pairs-k4_delta_in_0005.txt")

# Récupération des 8 premiers bits de K4 (chemin 0040 → 0606, masque 0x0F0F)
best_k4_mask1 = recover_k4_using_mask(pairs_k4_0606, expected_delta=0x0606, mask=0x0F0F)

# Récupération des 8 bits restants de K4 (chemin 0005 → a0a0, masque 0xF0F0)
best_k4_mask2 = recover_k4_using_mask(pairs_k4_a0a0, expected_delta=0xa0a0, mask=0xF0F0)

# Combinaison des deux parties pour obtenir la sous-clé complète K4
full_k4 = best_k4_mask1 | best_k4_mask2
print(f"Sous-clé K4 complète retrouvée : {full_k4:04x}")

'''
def recover_k3_using_mask(pairs, expected_delta, mask):
    """ Récupère 8 bits de K3 en utilisant un masque donné """
    scores = [0] * 65536  # 65536 possibilités pour les 16 bits de K3

    for k3 in range(65536):  # Tester toutes les valeurs possibles de K3 (16 bits)
        if k3 & ~mask != 0:  # On ignore les K3 qui ne respectent pas le masque
            continue

        score = 0
        for C, C_prime in pairs:
            # Annuler la sous-clé K3
            T = C ^ k3
            T_prime = C_prime ^ k3

            # Appliquer la S-Box inversée
            U = (s_inv[(T >> 12) & 0xF] << 12) | (s_inv[(T >> 8) & 0xF] << 8) | \
                (s_inv[(T >> 4) & 0xF] << 4) | (s_inv[T & 0xF])

            U_prime = (s_inv[(T_prime >> 12) & 0xF] << 12) | (s_inv[(T_prime >> 8) & 0xF] << 8) | \
                      (s_inv[(T_prime >> 4) & 0xF] << 4) | (s_inv[T_prime & 0xF])

            # Vérifier si la différence obtenue correspond à expected_delta
            if (U ^ U_prime) & mask == expected_delta:
                score += 1

        scores[k3] = score  # Sauvegarder le score pour cette clé

    best_k3 = max(range(65536), key=lambda k: scores[k])  # Trouver la meilleure clé K3
    print(f"Meilleure estimation pour K3 avec masque {mask:04x}: {best_k3:04x} (score = {scores[best_k3]})")
    return best_k3


# Chargement des paires de chiffrés pour K3
pairs_k3_0550 = read_cipher_pairs("pairs_k3_delta_in_0220.txt")
pairs_k3_a0a0 = read_cipher_pairs("pairs_k3_delta_in_1010.txt")

# Récupération des 8 premiers bits de K3 (chemin 0220 → 0550, masque 0x0F0F)
best_k3_mask1 = recover_k3_using_mask(pairs_k3_0550, expected_delta=0x0550, mask=0x0F0F)

# Récupération des 8 bits restants de K3 (chemin 1010 → A0A0, masque 0xF0F0)
best_k3_mask2 = recover_k3_using_mask(pairs_k3_a0a0, expected_delta=0xA0A0, mask=0xF0F0)

# Combinaison des deux parties pour obtenir la sous-clé complète K3
full_k3 = best_k3_mask1 | best_k3_mask2
print(f"Sous-clé K3 complète retrouvée : {full_k3:04x}")


def recover_k2(known_k3, pairs):
    """ Récupère K2 en remontant un round en arrière """
    scores = [0] * 65536  # 65536 possibilités pour les 16 bits de K2

    for k2 in range(65536):  # Tester toutes les valeurs possibles de K2
        score = 0
        for C, C_prime in pairs:
            # Annuler K3
            T = C ^ known_k3
            T_prime = C_prime ^ known_k3

            # Appliquer la S-Box inversée
            U = (s_inv[(T >> 12) & 0xF] << 12) | (s_inv[(T >> 8) & 0xF] << 8) | \
                (s_inv[(T >> 4) & 0xF] << 4) | (s_inv[T & 0xF])

            U_prime = (s_inv[(T_prime >> 12) & 0xF] << 12) | (s_inv[(T_prime >> 8) & 0xF] << 8) | \
                      (s_inv[(T_prime >> 4) & 0xF] << 4) | (s_inv[T_prime & 0xF])

            # Vérifier si la différence obtenue correspond à une propagation linéaire
            if (U ^ U_prime) == (C ^ C_prime):  
                score += 1

        scores[k2] = score  # Sauvegarder le score pour cette clé

    best_k2 = max(range(65536), key=lambda k: scores[k])  # Trouver la meilleure clé K2
    print(f"Sous-clé K2 retrouvée : {best_k2:04x} (score = {scores[best_k2]})")
    return best_k2


# Charger les paires de chiffrés pourprint(scores) K2
pairs_k2 = read_cipher_pairs("pairs-k2_delta_in_bbbb.txt")

# Récupération de K2
k2 = recover_k2(full_k3, pairs_k2)


def recover_k1(known_keys, plaintext, ciphertext):
    """ Récupère la sous-clé K1 en remontant tout le chiffrement """
    
    temp = ciphertext  # Commencer à partir du texte chiffré

    # Annuler K5
    temp ^= known_keys[4]

    # Annuler les 4 rounds en sens inverse
    for i in range(3, -1, -1):
        temp = decrypt_round(temp, known_keys[i], do_perm=(i < 3))

    # La valeur obtenue doit être égale au plaintext après annulation de K1
    k1 = temp ^ plaintext
    print(f"Sous-clé K1 retrouvée : {k1:04x}")
    return k1
'''