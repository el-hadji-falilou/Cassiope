############################################
# minicipher.py : skeleton file for part 1 #
############################################


##############
# Encryption #
##############


# S-Box Definition
s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]


# Permutation Definition
perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


# Execution of one encryption round (TODO)
def encrypt_round(input, key, do_perm):
    """encrypt_round
    Parameters
    ----------
    input   : the input block
    key     : the sub-key for this round
    do_perm : if True, perform the permutation (it is False for the last round)

    Output
    ------
    the output value for the round
    """
    if isinstance(input, str):
        input = int(input, 16) 

    # Subkey Addition
    post_subkey=input^key

    # S-Box Application
    binary = bin(post_subkey)[2:].zfill(16)
    blocks=[int(binary[i:i+4], 2) for i in range (0, 16, 4)]
    s_blocks=[s[block] for block in blocks]
    post_sbox=""
    for block in s_blocks:
        post_sbox+=bin(block)[2:].zfill(4)

    # If no permutation is performed, we can return the result early
    if do_perm==False:
        return int(post_sbox, 2)

    # Else, we perform the permutation
    else:
        post_perm=""
        for i in range (16):
            post_perm+=post_sbox[perm[i]]
        return int(post_perm, 2)



# Complete Encryption (TODO)
def encrypt(plaintext, keys):
    """encrypt
    Parameters
    ----------
    plaintext : input plaintext to encrypt
    keys      : array containing the 5 subkeys (i.e. the complete key)

    Output
    ------
    the encrypted value
    """
    output=encrypt_round(plaintext, keys[0], True)
    output=encrypt_round(output, keys[1], True)
    output=encrypt_round(output, keys[2], True)
    output=encrypt_round(output, keys[3], False)
    output = output ^ keys[4]
    return output



##############
# Decryption #
##############


# Inverse operations for S-Box and Permutation
s_inv = [0] * 16
perm_inv = [0] * 16


# Compute the reverse S-Box and Permutation (TODO)


def init_inverse_ops():
    """This function populates  s_inv et perm_inv to make decryption possible.
    Of course, it should be called BEFORE any decryption operation.
    """
    for i in range (16):
        s_inv[s[i]]=i
        perm_inv[perm[i]] = i



# One Decryption round (TODO)
def decrypt_round(input, key, do_perm):
    """decrypt_round
    Parameters
    ----------
    input   : the ciphertext block to decrypt
    key     : round subkey
    do_perm : if True, perform the permutation

    Output
    ------
    The decrypted plaintext value
    """
    if isinstance(input, int):  
        binary=bin(input)[2:].zfill(16)
    
    if isinstance(input, str):  
        if input.startswith("0b"):  
            binary=input[2:].zfill(16)
        else:
            binary=bin(int(input, 16))[2:].zfill(16)

    if do_perm==True:
        post_perm=""
        for i in range (16):
            post_perm+=binary[perm_inv[i]]
    else:
        post_perm=binary

    blocks=[int(post_perm[i:i+4], 2) for i in range (0, 16, 4)]
    s_blocks=[s_inv[block] for block in blocks]
    post_sbox=""
    for block in s_blocks:
        post_sbox+=bin(block)[2:].zfill(4)

    post_subkey=int(post_sbox, 2)^key

    return post_subkey




# Complete Decryption (TODO)
def decrypt(ciphertext, keys):
    """decrypt
    Parameters
    ----------
    ciphertext : ciphertext to decrypt
    keys       : array containing the 5 subkeys (i.e. the complete key)

    Output
    ------
    The decrypted plaintext
    """
    output = ciphertext ^ keys[4]
    output=decrypt_round(output, keys[3], False)
    output=decrypt_round(output, keys[2], True)
    output=decrypt_round(output, keys[1], True)
    output=decrypt_round(output, keys[0], True)
    return output