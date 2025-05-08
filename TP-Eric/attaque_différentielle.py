#!/usr/bin/env python3

from minicipher import decrypt_round
from minicipher import decrypt

###############################################################################
# 1) Définition de la S-Box et de son inverse
###############################################################################
s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

s_inv = [0]*16
for i in range(16):
    s_inv[s[i]] = i

###############################################################################
# 2) Définition de la permutation et de son inverse
###############################################################################
def perm_inverse(x):
    """
    Applique l'inverse de la permutation de MiniCipher sur un entier 16 bits.
    """
    perm = [0,  4,  8, 12, 1,  5,  9, 13, 2,  6, 10, 14, 3,  7, 11, 15]
    perm_inv = [0]*16
    for i, p in enumerate(perm):
        perm_inv[p] = i  # Génère la table d'inversion de permutation

    result = 0
    for bitpos in range(16):
        if (x >> bitpos) & 1:  # Vérifie si le bit est à 1
            result |= (1 << perm_inv[bitpos])  # Replace le bit à sa position inversée
    return result

###############################################################################
# 3) Lecture des paires de chiffrés
###############################################################################
def read_cipher_pairs(filename):
    """ Lit un fichier, Retourne une liste de tuples (C, C') en int."""
    pairs = []
    with open(filename, "r") as f:
        for line in f:
            c_str, cprime_str = line.strip().split(", ")
            c_str = c_str.strip()
            cprime_str = cprime_str.strip()
            c_val = int(c_str, 16)
            cprime_val = int(cprime_str, 16)
            pairs.append((c_val, cprime_val))
    return pairs

###############################################################################
# 4) Récupération de K5
###############################################################################
def recover_k5_using_mask(pairs, expected_delta, mask):
    """
    Récupère 8 bits (ou 16 bits par blocs de 8) de K5,
    en se basant sur un chemin différentiel menant à 'expected_delta' sur 'mask'.
    """
    scores = [0]*65536
    for k5 in range(65536):
        if k5 & ~mask != 0:
            continue

        score = 0
        for C, C_prime in pairs:
            T = C ^ k5
            T_prime = C_prime ^ k5

            # Inverser la dernière S-Box
            U = 0
            U_prime = 0
            for i in range(4):
                shift = 4*i
                q  = (T >> shift) & 0xF
                qp = (T_prime >> shift) & 0xF
                U       |= (s_inv[q]  << shift)
                U_prime |= (s_inv[qp] << shift)

            # Vérifier la différence sur le masque
            if (U ^ U_prime) == expected_delta:
                score += 1

        scores[k5] = score

    best_k5 = max(range(65536), key=lambda k: scores[k])
    print(f"Sous-clé K5 retrouvée : {best_k5:04x} (score={scores[best_k5]})")
    return best_k5

pairs_0606 = read_cipher_pairs("pairs-k5_0b00_0606.txt")
pairs_a0a0 = read_cipher_pairs("pairs-k5_000d_a0a0.txt")
best_k5_mask1 = recover_k5_using_mask(pairs_0606, expected_delta=0x0606, mask=0x0F0F)
best_k5_mask2 = recover_k5_using_mask(pairs_a0a0, expected_delta=0xa0a0, mask=0xF0F0)
full_k5 = best_k5_mask1 | best_k5_mask2
print(f"Sous-clé K5 complète retrouvée : {full_k5:04x}\n")

###############################################################################
# 5) Récupération de K4
###############################################################################
def recover_k4_using_mask(pairs, expected_delta, mask, k5):
    """
    Récupère 8 bits (ou 16 bits par blocs de 8) de K4,
    en se basant sur un chemin différentiel menant à 'expected_delta' sur 'mask'.
    Utilise la sous-clé k5 déjà retrouvée.
    """
    #Pour chaque sous-clé possible k4, Si k AND NOT mask != 0, Alors on passe au k suivant
    scores = [0]*65536 
    for k4 in range(65536):
        if k4 & ~mask != 0:
            continue

        score = 0
        for C, C_prime in pairs:
            # Étape 1 : XOR avec K5 (connue)
            X  = C ^ k5
            Xp = C_prime ^ k5

            # Étape 2 : Application inverse des dernières S-boxes
            U = U_prime = 0
            for i in range(4):
                shift = 4*i
                q  = (X >> shift) & 0xF
                qp = (Xp >> shift) & 0xF
                U       |= (s_inv[q] << shift)
                U_prime |= (s_inv[qp] << shift)

            # Étape 3 : XOR avec K4 
            V  = U ^ k4
            Vp = U_prime ^ k4

            # Étape 4 : Inversion de la permutation
            W  = perm_inverse(V)
            Wp = perm_inverse(Vp)

            # Étape 5 : Inversion des avant-dernières S-Boxes
            Z = Z_prime = 0
            for i in range(4):
                shift = 4*i
                q  = (W >> shift) & 0xF
                qp = (Wp >> shift) & 0xF
                Z       |= (s_inv[q] << shift)
                Z_prime |= (s_inv[qp] << shift)

            # Vérifier la différence attendue avec le masque
            if (Z ^ Z_prime) == expected_delta:
                score += 1

        scores[k4] = score

    best_k4 = max(range(65536), key=lambda k: scores[k])
    print(f"Sous-clé K4 retrouvée (masque {mask:04x}) : {best_k4:04x} (score={scores[best_k4]})")
    return best_k4

# Lecture des paires pour K4
pairs_k4_0040 = read_cipher_pairs("pairs-k4_0040.txt")
pairs_k4_0005 = read_cipher_pairs("pairs-k4_0005.txt")

# Application des deux masques pour récupérer K4
best_k4_mask1 = recover_k4_using_mask(pairs_k4_0040, expected_delta=0x0606, mask=0x5555, k5=full_k5)
best_k4_mask2 = recover_k4_using_mask(pairs_k4_0005, expected_delta=0xa0a0, mask=0xAAAA, k5=full_k5)

full_k4 = best_k4_mask1 | best_k4_mask2
print(f"Sous-clé K4 complète retrouvée : {full_k4:04x}\n")
print(" ")

###############################################################################
# 6) Récupération de K3
###############################################################################
def recover_k3_using_mask(pairs, expected_delta, mask, known_k5, known_k4):
    """
    Récupère 8 bits (ou 16 bits par blocs de 8) de K3,
    en se basant sur un chemin différentiel menant à 'expected_delta' sur 'mask'.
    Utilise les sous-clés K5 et K4 déjà retrouvées.
    """
    scores = [0]*65536
    for k3 in range(65536):
        if (k3 & ~mask) != 0:
            continue  # Ignore les valeurs de k3 qui ne respectent pas le masque

        score = 0
        for (C, Cprime) in pairs:
            # Étape 1 : Annuler K5
            T  = C  ^ known_k5
            Tp = Cprime ^ known_k5

            # Étape 2 : Inverser la dernière S-Box
            U  = 0
            Up = 0
            for i in range(4):
                shift = 4*i
                U  |= (s_inv[(T  >> shift) & 0xF]  << shift)
                Up |= (s_inv[(Tp >> shift) & 0xF] << shift)

            # Étape 3 : Annuler K4
            V  = U  ^ known_k4
            Vp = Up ^ known_k4

            # Étape 4 : Inverser la permutation
            W  = perm_inverse(V)
            Wp = perm_inverse(Vp)

            # Étape 5 : Inverser l'avant-dernière S-Box
            X  = 0
            Xp = 0
            for i in range(4):
                shift = 4*i
                X  |= (s_inv[(W  >> shift) & 0xF]  << shift)
                Xp |= (s_inv[(Wp >> shift) & 0xF] << shift)

            # Étape 6 : XOR avec K3 (on teste cette clé candidate)
            Y  = X  ^ k3
            Yp = Xp ^ k3

            # Étape 7 : Inverser la permutation
            Z  = perm_inverse(Y)
            Zp = perm_inverse(Yp)

            # Étape 8 : Inverser la S-Box avant avant-dernière
            T3  = 0
            T3p = 0
            for i in range(4):
                shift = 4*i
                T3  |= (s_inv[(Z  >> shift) & 0xF]  << shift)
                T3p |= (s_inv[(Zp >> shift) & 0xF] << shift)

            # Étape 9 : Vérifier la différence attendue avec le masque
            if (T3 ^ T3p) == expected_delta:
                score += 1

        scores[k3] = score
    best_k3 = max(range(65536), key=lambda k: scores[k])
    print(f"[K3] Meilleure clé partielle (mask={mask:04x}) => {best_k3:04x} (score={scores[best_k3]})")
    return best_k3

# Lecture des paires pour K3
pairs_k3_0606 = read_cipher_pairs("pairs_k3_delta_in_0220.txt")
pairs_k3_a0a0 = read_cipher_pairs("pairs_k3_delta_in_1010.txt")

# Application des deux masques spécifiés par l'enseignant pour récupérer K3
best_k3_mask1 = recover_k3_using_mask(pairs_k3_0606, expected_delta=0x0606, mask=0x5555, known_k5=full_k5, known_k4=full_k4)
best_k3_mask2 = recover_k3_using_mask(pairs_k3_a0a0, expected_delta=0xa0a0, mask=0xAAAA, known_k5=full_k5, known_k4=full_k4)

# Fusion des deux parties de K3
full_k3 = best_k3_mask1 | best_k3_mask2
print(f"Sous-clé K3 complète retrouvée : {full_k3:04x}\n")
print(" ")


###############################################################################
# 7) Récupération de K2 
###############################################################################
def recover_k2(known_k5, known_k4, known_k3, pairs):
    """
    Récupère K2 en remontant un tour du chiffrement.
    Le chemin différentiel a une probabilité de 1, donc l'expected_delta est exactement
    la différence initiale utilisée dans le fichier de paires.
    """
    scores = [0]*65536
    expected_delta = 0xBBBB  

    for k2 in range(65536):
        if (k2 & ~0xFFFF) != 0:
            continue  # Ignore les valeurs hors du masque

        score = 0
        for (C, Cprime) in pairs:
            # Étape 1 : Annuler K5
            T  = C  ^ known_k5
            Tp = Cprime ^ known_k5

            # Étape 2 : Inverser la dernière S-Box
            U = 0
            Up = 0
            for i in range(4):
                shift = 4*i
                U  |= (s_inv[(T  >> shift) & 0xF]  << shift)
                Up |= (s_inv[(Tp >> shift) & 0xF] << shift)

            # Étape 3 : Annuler K4
            V  = U  ^ known_k4
            Vp = Up ^ known_k4

            # Étape 4 : Inverser la permutation
            W  = perm_inverse(V)
            Wp = perm_inverse(Vp)

            # Étape 5 : Inverser l'avant-dernière S-Box
            X  = 0
            Xp = 0
            for i in range(4):
                shift = 4*i
                X  |= (s_inv[(W  >> shift) & 0xF]  << shift)
                Xp |= (s_inv[(Wp >> shift) & 0xF] << shift)

            # Étape 6 : Annuler K3
            Y  = X  ^ known_k3
            Yp = Xp ^ known_k3

            # Étape 7 : Inverser la permutation
            Z  = perm_inverse(Y)
            Zp = perm_inverse(Yp)

            # Étape 8 : Inverser la S-Box avant avant-dernière
            T3  = 0
            T3p = 0
            for i in range(4):
                shift = 4*i
                T3  |= (s_inv[(Z  >> shift) & 0xF]  << shift)
                T3p |= (s_inv[(Zp >> shift) & 0xF] << shift)

            # Étape 9 : XOR avec K2 (clé candidate)
            W_final  = T3  ^ k2
            Wp_final = T3p ^ k2

            # Étape 10 : Inverser la permutation (tour -4)
            Z_final  = perm_inverse(W_final)
            Zp_final = perm_inverse(Wp_final)

            # Étape 11 : Inverser la S-Box du tour -4
            T4  = 0
            T4p = 0
            for i in range(4):
                shift = 4*i
                T4  |= (s_inv[(Z_final  >> shift) & 0xF]  << shift)
                T4p |= (s_inv[(Zp_final >> shift) & 0xF] << shift)

            # Étape 12 : Vérification finale avec expected_delta
            if (T4 ^ T4p) == expected_delta:
                score += 1

        scores[k2] = score

    best_k2 = max(range(65536), key=lambda k: scores[k])
    print(f"Sous-clé K2 retrouvée : {best_k2:04x} (score={scores[best_k2]})")
    return best_k2

# Lecture des paires pour K2
pairs_k2 = read_cipher_pairs("pairs-k2_delta_in_bbbb.txt")  # Vérifie le bon fichier

# Récupération de K2
full_k2 = recover_k2(full_k5, full_k4, full_k3, pairs_k2)

print(f"Sous-clé K2 complète retrouvée : {full_k2:04x}\n")
print(" ")

###############################################################################
# 8) Récupération de K1 via (plaintext, ciphertext)
###############################################################################
def recover_k1(known_k5, known_k4, known_k3, known_k2, pairs):
    """
    Récupère K1 en remontant tous les tours du chiffrement.
    Utilise un couple (plaintext, ciphertext).
    """
    scores = [0]*65536

    for k1 in range(65536):  # Tester toutes les valeurs possibles de K1 (16 bits)
        score = 0
        for (plaintext, ciphertext) in pairs:
            # Étape 1 : Annuler K5
            T  = ciphertext ^ known_k5

            # Étape 2 : Inverser la dernière S-Box
            U = 0
            for i in range(4):
                shift = 4*i
                U |= (s_inv[(T >> shift) & 0xF] << shift)

            # Étape 3 : Annuler K4
            V  = U ^ known_k4

            # Étape 4 : Inverser la permutation
            W  = perm_inverse(V)

            # Étape 5 : Inverser l'avant-dernière S-Box
            X  = 0
            for i in range(4):
                shift = 4*i
                X |= (s_inv[(W >> shift) & 0xF] << shift)

            # Étape 6 : Annuler K3
            Y  = X ^ known_k3

            # Étape 7 : Inverser la permutation
            Z  = perm_inverse(Y)

            # Étape 8 : Inverser la S-Box avant avant-dernière
            T3  = 0
            for i in range(4):
                shift = 4*i
                T3 |= (s_inv[(Z >> shift) & 0xF] << shift)

            # Étape 9 : Annuler K2
            W_final  = T3 ^ known_k2

            # Étape 10 : Inverser la permutation (tour -4)
            Z_final  = perm_inverse(W_final)

            # Étape 11 : Inverser la S-Box du tour -4
            T4  = 0
            for i in range(4):
                shift = 4*i
                T4 |= (s_inv[(Z_final >> shift) & 0xF] << shift)

            # Étape 12 : Vérification (T4 XOR k1 doit donner plaintext)
            if (T4 ^ k1) == plaintext:
                score += 1

        scores[k1] = score

    best_k1 = max(range(65536), key=lambda k: scores[k])
    print(f"Sous-clé K1 retrouvée : {best_k1:04x} (score={scores[best_k1]})")
    return best_k1

###############################################################################
# Chargement du fichier contenant un couple (plaintext, ciphertext)
###############################################################################
def read_plaintext_ciphertext(filename):
    """
    Lit un fichier contenant une ligne ex: "0123, abcd"
    et retourne une liste [(plaintext, ciphertext)] en int.
    """
    pairs = []
    with open(filename, "r") as f:
        for line in f:
            p_str, c_str = line.strip().split(", ")
            pairs.append((int(p_str, 16), int(c_str, 16)))
    return pairs

# Lecture du fichier contenant un couple connu (plaintext, ciphertext)
pairs_k1 = read_plaintext_ciphertext("plaintext-ciphertext.txt")

# Récupération de K1
full_k1 = recover_k1(full_k5, full_k4, full_k3, full_k2, pairs_k1)
print(f"Sous-clé K1 complète retrouvée : {full_k1:04x}\n")

###############################################################################
# 9) Déchiffrement du message en mode CBC
###############################################################################
def decrypt_cbc(ciphertext_blocks, key_schedule, iv):
    """
    Déchiffre un message en mode CBC avec MiniCipher.
    
    - ciphertext_blocks : liste des blocs chiffrés en hexadécimal.
    - key_schedule : liste des sous-clés (K1 → K5) utilisées pour MiniCipher.
    - iv : vecteur d'initialisation.
    
    Retourne la liste des blocs du message déchiffré.
    """
    plaintext_blocks = []
    previous_block = iv

    for C in ciphertext_blocks:
        # Étape 1 : Déchiffrer le bloc avec MiniCipher
        P_temp = decrypt(C, key_schedule)  
        
        # Étape 2 : XOR avec le bloc précédent (ou IV pour le premier bloc)
        P = P_temp ^ previous_block  

        # Stocker le texte clair déchiffré
        plaintext_blocks.append(P)

        # Mise à jour du bloc précédent pour le prochain tour
        previous_block = C  

    return plaintext_blocks

###############################################################################
# Lecture du fichier message.xyz contenant les blocs chiffrés
###############################################################################
def load_ciphertext(filename):
    """
    Charge un fichier contenant des blocs chiffrés en mode binaire (16 bits).
    Retourne une liste d'entiers 16 bits extraits des paires d'octets.
    """
    with open(filename, "rb") as f:  # ✅ Lecture en binaire
        data = f.read()  # Lire tout le fichier

    # ✅ Convertir chaque 2 octets (16 bits) en un entier
    ciphertext_blocks = [int.from_bytes(data[i:i+2], byteorder='little') for i in range(0, len(data), 2)]

    return ciphertext_blocks

# Charger les blocs chiffrés depuis message.xyz
ciphertext = load_ciphertext("message.xyz")

# Définition de l'IV (vecteur d'initialisation)
iv = 0x0000  # ⚠ Vérifie que c'est bien l'IV donné dans le TP

# Création de la clé complète sous forme de liste [K1, K2, K3, K4, K5]
key_schedule = [full_k5, full_k4, full_k3, full_k2, full_k1]

# Déchiffrement en mode CBC
plaintext_blocks = decrypt_cbc(ciphertext, key_schedule, iv)

###############################################################################
# Affichage du message déchiffré en ASCII
###############################################################################
def convert_to_ascii(plaintext_blocks):
    """
    Convertit une liste de blocs 16 bits en une chaîne de texte ASCII.
    """
    message = ""
    for block in plaintext_blocks:
        # Extraire les 2 caractères ASCII par bloc de 16 bits (chaque octet = 8 bits)
        char1 = (block >> 8) & 0xFF  # Premier caractère
        char2 = block & 0xFF  # Deuxième caractère
        message += chr(char1) + chr(char2)

    return message

# Convertir les blocs en texte ASCII
decrypted_message = convert_to_ascii(plaintext_blocks)

# Afficher le message final
print("\n🔓 Message déchiffré :")
print(decrypted_message)
