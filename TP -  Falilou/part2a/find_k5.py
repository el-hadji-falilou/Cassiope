s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

s_inv = [0] * 16
for i in range (16):
    s_inv[s[i]]=i

# 0b00 --> 0606
file_path = "../crypto-material/pairs-k5_0b00_0606.txt"
k5_1=("0000", 0)

for i in range(256):
    key = ((i & 0x0F) | ((i & 0xF0) << 4))
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
            if xor_result=="0606":
                count+=1
    # On prend la sous-clés qui marche avec le plus de couples (C, C')
    if count>k5_1[1]:         
        k5_1=(key, count)

# 000d --> a0a0
file_path = "../crypto-material/pairs-k5_000d_a0a0.txt"
k5_2=("0000", 0)

for i in range(256):
    key = ((i & 0x0F) << 4) | ((i & 0xF0) << 8)
    count=0

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            C_1, C_2 = line.split(", ")
            T_1=int(C_1, 16)^key
            T_2=int(C_2, 16)^key
            
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

            xor_result=hex(int(U_1, 2)^int(U_2, 2))[2:].zfill(4).upper()

            if xor_result=="A0A0":
                count+=1

    if count>k5_2[1]:         
        k5_2=(key, count)

k5=hex(k5_1[0]^k5_2[0])[2:].zfill(4)

print(hex(k5_1[0])[2:].zfill(4), k5_1[1])
print(hex(k5_2[0])[2:].zfill(4), k5_2[1])
print(k5)