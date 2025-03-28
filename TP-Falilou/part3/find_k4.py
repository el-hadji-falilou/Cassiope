s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

s_inv = [0] * 16
perm_inv = [0] * 16
for i in range (16):
    s_inv[s[i]]=i
    perm_inv[s[i]]=i

k5=0x5d8e

# 0040 --> 0606
file_path = "../crypto-material/pairs-k4_delta_in_0040.txt"
k4_1=("0000", 0)
mask=0x5555
for key in range(2**16):
    if (key & ~mask) != 0:
        continue
    count=0

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            C_1, C_2 = line.split(", ")

            # On applique la sous-clé K5-
            T_1=int(C_1, 16)^k5
            T_2=int(C_2, 16)^k5

            # On applique la S-box inversée
            binary = bin(T_1)[2:].zfill(16)
            blocks=[int(binary[i:i+4], 2) for i in range (0, 16, 4)]
            s_blocks=[s_inv[block] for block in blocks]
            U_1=""
            for block in s_blocks:
                U_1+=bin(block)[2:].zfill(4)
            binary = bin(T_2)[2:].zfill(16)
            blocks=[int(binary[i:i+4], 2) for i in range (0, 16, 4)]
            s_blocks=[s_inv[block] for block in blocks]
            U_2=""
            for block in s_blocks:
                U_2+=bin(block)[2:].zfill(4)

            # On applique la sous-clé
            V_1=int(U_1, 16)^key
            V_2=int(U_2, 16)^key

            # Permutation
            binary = bin(V_1)[2:].zfill(16)
            W_1 = list(bin(0)[2:].zfill(16))
            for i in range (16):
                W_1[perm_inv[i]]=binary[i]
            W_1=''.join(W_1)
            binary = bin(V_2)[2:].zfill(16)
            W_2=list(bin(0)[2:].zfill(16))
            for i in range (16):
                W_2[perm_inv[i]]=binary[i]
            W_2=''.join(W_2)

            # On applique la S-box inversée
            blocks=[int(W_1[i:i+4], 2) for i in range (0, 16, 4)]
            s_blocks=[s_inv[block] for block in blocks]
            W_1=""
            for block in s_blocks:
                W_1+=bin(block)[2:].zfill(4)
            blocks=[int(W_2[i:i+4], 2) for i in range (0, 16, 4)]
            s_blocks=[s_inv[block] for block in blocks]
            W_2=""
            for block in s_blocks:
                W_2+=bin(block)[2:].zfill(4)

            # On calcule la différence entre W_1 et W_2 pour vérifier si la sous-clé marche
            xor_result=hex(int(W_1, 2)^int(W_2, 2))[2:].zfill(4).upper()
            if xor_result=="0606":
                count+=1

    # On prend la sous-clés qui marche avec le plus de couples (C, C')
    if count>k4_1[1]:        
        k4_1=(key, count)

# 0005 --> a0a0
file_path = "../crypto-material/pairs-k4_delta_in_0005.txt"
k4_2=("0000", 0)
mask=0x5555
for key in range(2**16):
    if (key & ~mask) != 0:
        continue
    count=0

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            C_1, C_2 = line.split(", ")

            # On applique la sous-clé
            T_1=int(C_1, 16)^key
            T_2=int(C_2, 16)^key
            
            # On applique la S-box inversée
            binary = bin(T_1)[2:].zfill(16)
            blocks=[int(binary[i:i+4], 2) for i in range (0, 16, 4)]
            s_blocks=[s_inv[block] for block in blocks]
            U_1=""
            for block in s_blocks:
                U_1+=bin(block)[2:].zfill(4)
            
            binary = bin(T_2)[2:].zfill(16)
            blocks=[int(binary[i:i+4], 2) for i in range (0, 16, 4)]
            s_blocks=[s_inv[block] for block in blocks]
            U_2=""
            for block in s_blocks:
                U_2+=bin(block)[2:].zfill(4)

            # On calcule la différence entre U_1 et U_2 pour vérifier si la sous-clé marche
            xor_result=hex(int(U_1, 2)^int(U_2, 2))[2:].zfill(4).upper()
            if xor_result=="A0A0":
                count+=1

    # On prend la sous-clés qui marche avec le plus de couples (C, C')
    if count>k4_2[1]:
        k4_2=(key, count)

print(k4_1[0], k4_1[1])
print(k4_2[0], k4_2[1])