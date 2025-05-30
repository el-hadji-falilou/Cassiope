##### START_QUESTION_8 #####
s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

global s_inv, perm_inv
s_inv = [0]*16
perm_inv = [0]*16

def init_inverse_ops():
    """This function populates  s_inv et perm_inv to make decryption possible.
    Of course, it should be called BEFORE any decryption operation.
    """
    # Calcul de l'inverse de la S-Box
    for i in range(16):
        s_inv[s[i]] = i
    
    # Calcul de l'inverse de la permutation
    for i in range(16):
        perm_inv[perm[i]] = i

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

def read_cipher_pairs(filename):
    """Reads a text file containing (C, C') pairs in hexadecimal
    and returns a list of (int, int) tuples."""
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

def find_k5_part1() -> int:
    """
    Trouve les 8 bits de k5 (masque 0x0F0F) en testant :
        1. Toutes les clés candidates 8 bits
        2. Pour chaque paire (C, C') dans pairs-k5_0b00_0606.txt, vérifie si C⊕k5 et C'⊕k5 donnent le Δ attendu après S-box inverse

    Retourne la clé avec le plus de succès
    """
    pairs = read_cipher_pairs("pairs_k5_0b00_0606.txt")
    mask = 0x0F0F
    expected_delta = 0x0606
    scores = [0] * 65536
    for k5 in range(65536):
        if k5 & ~mask != 0:
            continue
        score = 0
        for C, C_prime in pairs:
            T = C ^ k5
            Tp = C_prime ^ k5
            U = U_prime = 0
            for i in range(4):
                shift = 4 * i
                U |= s_inv[(T >> shift) & 0xF] << shift
                U_prime |= s_inv[(Tp >> shift) & 0xF] << shift
            if (U ^ U_prime) == expected_delta:
                score += 1
        scores[k5] = score
    return max(range(65536), key=lambda k: scores[k])
##### END_QUESTION_8 #####



##### START_QUESTION_9 #####
def find_k5_part2() -> int:
    """
    Trouve les 8 bits de k5 (masque 0xF0F0) en testant :
        1. Toutes les clés candidates 8 bits
        2. Pour chaque paire (C, C') dans pairs-k5_000d_a0a0.txt, vérifie si C⊕k5 et C'⊕k5 donnent le Δ attendu après S-box inverse

    Retourne la clé avec le plus de succès
    """
    pairs = read_cipher_pairs("pairs_k5_000d_a0a0.txt")
    mask = 0xF0F0
    expected_delta = 0xA0A0
    scores = [0] * 65536
    for k5 in range(65536):
        if k5 & ~mask != 0:
            continue
        score = 0
        for C, C_prime in pairs:
            T = C ^ k5
            Tp = C_prime ^ k5
            U = U_prime = 0
            for i in range(4):
                shift = 4 * i
                U |= s_inv[(T >> shift) & 0xF] << shift
                U_prime |= s_inv[(Tp >> shift) & 0xF] << shift
            if (U ^ U_prime) == expected_delta:
                score += 1
        scores[k5] = score
    return max(range(65536), key=lambda k: scores[k])
##### END_QUESTION_9 #####



##### START_QUESTION_12 #####
def find_k4_part1() -> int:
    """
    Trouve 8 bits de k4 (masque 0x5555) en testant :
        1. Toutes les clés candidates 8 bits
        2. Pour chaque paire (C, C') dans pairs-k4_0040_0606.txt,
           vérifie si C⊕k4 et C'⊕k4 donnent Δ=0x0606 après S-box inverse

    Retourne la clé avec le plus de succès
    """
    k5 = find_k5_part1() | find_k5_part2()
    pairs = read_cipher_pairs("pairs_k4_0040.txt")
    mask = 0x5555
    expected_delta = 0x0606
    scores = [0] * 65536
    for k4 in range(65536):
        if k4 & ~mask != 0:
            continue
        score = 0
        for C, C_prime in pairs:
            X = C ^ k5
            Xp = C_prime ^ k5
            U = U_prime = 0
            for i in range(4):
                shift = 4 * i
                U |= s_inv[(X >> shift) & 0xF] << shift
                U_prime |= s_inv[(Xp >> shift) & 0xF] << shift
            V = U ^ k4
            Vp = U_prime ^ k4
            W = perm_inverse(V)
            Wp = perm_inverse(Vp)
            Z = Z_prime = 0
            for i in range(4):
                shift = 4 * i
                Z |= s_inv[(W >> shift) & 0xF] << shift
                Z_prime |= s_inv[(Wp >> shift) & 0xF] << shift
            if (Z ^ Z_prime) == expected_delta:
                score += 1
        scores[k4] = score
    return max(range(65536), key=lambda k: scores[k])


def find_k4_part2() -> int:
    """
    Trouve 8 bits de k4 (masque 0xAAAA) en testant :
        1. Toutes les clés candidates 8 bits
        2. Pour chaque paire (C, C') dans pairs-k4_0005_a0a0.txt,
           vérifie si C⊕k4 et C'⊕k4 donnent Δ=0xA0A0 après S-box inverse

    Retourne la clé avec le plus de succès
    """
    k5 = find_k5_part1() | find_k5_part2()
    pairs = read_cipher_pairs("pairs_k4_0005.txt")
    mask = 0xAAAA
    expected_delta = 0xA0A0
    scores = [0] * 65536
    for k4 in range(65536):
        if k4 & ~mask != 0:
            continue
        score = 0
        for C, C_prime in pairs:
            X = C ^ k5
            Xp = C_prime ^ k5
            U = U_prime = 0
            for i in range(4):
                shift = 4 * i
                U |= s_inv[(X >> shift) & 0xF] << shift
                U_prime |= s_inv[(Xp >> shift) & 0xF] << shift
            V = U ^ k4
            Vp = U_prime ^ k4
            W = perm_inverse(V)
            Wp = perm_inverse(Vp)
            Z = Z_prime = 0
            for i in range(4):
                shift = 4 * i
                Z |= s_inv[(W >> shift) & 0xF] << shift
                Z_prime |= s_inv[(Wp >> shift) & 0xF] << shift
            if (Z ^ Z_prime) == expected_delta:
                score += 1
        scores[k4] = score
    return max(range(65536), key=lambda k: scores[k])
##### END_QUESTION_12 #####



##### START_QUESTION_14 #####
def find_k3_part1() -> int:
    """
    Trouve 8 bits de k3 (masque 0x3333) en testant :
        1. Toutes les clés candidates 8 bits
        2. Pour chaque paire (C, C') dans pairs-k3_0220_????.txt,
           vérifie si C⊕k3 et C'⊕k3 donnent Δ attendu après S-box inverse

    Retourne la clé avec le plus de succès
    """
    k5 = find_k5_part1() | find_k5_part2()
    k4 = find_k4_part1() | find_k4_part2()
    pairs = read_cipher_pairs("pairs_k3_0220.txt")
    mask = 0x3333
    expected_delta = 0x0606
    scores = [0] * 65536
    for k3 in range(65536):
        if k3 & ~mask != 0:
            continue
        score = 0
        for C, C_prime in pairs:
            T = C ^ k5
            Tp = C_prime ^ k5
            U = U_prime = 0
            for i in range(4):
                shift = 4 * i
                U |= s_inv[(T >> shift) & 0xF] << shift
                U_prime |= s_inv[(Tp >> shift) & 0xF] << shift
            V = U ^ k4
            Vp = U_prime ^ k4
            W = perm_inverse(V)
            Wp = perm_inverse(Vp)
            X = X_prime = 0
            for i in range(4):
                shift = 4 * i
                X |= s_inv[(W >> shift) & 0xF] << shift
                X_prime |= s_inv[(Wp >> shift) & 0xF] << shift
            Y = X ^ k3
            Yp = X_prime ^ k3
            Z = perm_inverse(Y)
            Zp = perm_inverse(Yp)
            T3 = T3_prime = 0
            for i in range(4):
                shift = 4 * i
                T3 |= s_inv[(Z >> shift) & 0xF] << shift
                T3_prime |= s_inv[(Zp >> shift) & 0xF] << shift
            if (T3 ^ T3_prime) == expected_delta:
                score += 1
        scores[k3] = score
    return max(range(65536), key=lambda k: scores[k])


def find_k3_part2() -> int:
    """
    Trouve 8 bits de k3 (masque 0xCCCC) en testant :
        1. Toutes les clés candidates 8 bits
        2. Pour chaque paire (C, C') dans pairs-k3_1010_????.txt,
           vérifie si C⊕k3 et C'⊕k3 donnent Δ attendu après S-box inverse

    Retourne la clé avec le plus de succès
    """
    k5 = find_k5_part1() | find_k5_part2()
    k4 = find_k4_part1() | find_k4_part2()
    pairs = read_cipher_pairs("pairs_k3_1010.txt")
    mask = 0xCCCC
    expected_delta = 0xA0A0
    scores = [0] * 65536
    for k3 in range(65536):
        if k3 & ~mask != 0:
            continue
        score = 0
        for C, C_prime in pairs:
            T = C ^ k5
            Tp = C_prime ^ k5
            U = U_prime = 0
            for i in range(4):
                shift = 4 * i
                U |= s_inv[(T >> shift) & 0xF] << shift
                U_prime |= s_inv[(Tp >> shift) & 0xF] << shift
            V = U ^ k4
            Vp = U_prime ^ k4
            W = perm_inverse(V)
            Wp = perm_inverse(Vp)
            X = X_prime = 0
            for i in range(4):
                shift = 4 * i
                X |= s_inv[(W >> shift) & 0xF] << shift
                X_prime |= s_inv[(Wp >> shift) & 0xF] << shift
            Y = X ^ k3
            Yp = X_prime ^ k3
            Z = perm_inverse(Y)
            Zp = perm_inverse(Yp)
            T3 = T3_prime = 0
            for i in range(4):
                shift = 4 * i
                T3 |= s_inv[(Z >> shift) & 0xF] << shift
                T3_prime |= s_inv[(Zp >> shift) & 0xF] << shift
            if (T3 ^ T3_prime) == expected_delta:
                score += 1
        scores[k3] = score
    return max(range(65536), key=lambda k: scores[k])
##### END_QUESTION_14 #####



##### START_QUESTION_15 #####

##### END_QUESTION_15 #####
