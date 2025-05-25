############################################
# minicipher.py : skeleton file for part 1 #
############################################


##############
# Encryption #
##############


##### START_QUESTION_1 #####
# S-Box
s = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]


# Permutation
perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


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
     # Étape 1 : Ou exclusif avec la sous-clé (XOR)
     temp = input ^ key

     # Étape 2 : Application de la S-Box
     temp_sbox = 0 #variable qui stockera le résultat final après application de la S-Box
     for i in range(4):
          quartet = (temp >> (4 * i)) & 0xF  # Extraction du quartet
          new_quartet = s[quartet]  # Remplacement via la S-Box
          temp_sbox |= (new_quartet << (4 * i))  # Reconstruction du mot

     # Étape 3 : Vérifier si la permutation doit être appliquée
     if not do_perm:
          return temp_sbox

     temp_perm = 0
     # Étape 4 : Application de la permutation
     for i in range(16):
          bit = (temp_sbox >> i) & 1  # On extrait le bit à la position i de temp_sbox
          temp_perm |= (bit << perm[i])  # Placement à la position permutée

     return temp_perm


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
     # Initialisation de la variable temporaire
     temp = plaintext

     # 4 tours de chiffrement (les 3 premiers avec permutation, le dernier sans permutation)
     for i in range(4):
          temp = encrypt_round(temp, keys[i], do_perm=(i < 3))

     # Ajout de la dernière sous-clé après les 4 rounds
     temp ^= keys[4]

     return temp
##### END_QUESTION_1 #####


##### START_QUESTION_2 #####
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
     # Initialisation de la variable temporaire
     temp = plaintext

     # 4 tours de chiffrement (les 3 premiers avec permutation, le dernier sans permutation)
     for i in range(4):
          temp = encrypt_round(temp, keys[i], do_perm=(i < 3))

     # Ajout de la dernière sous-clé après les 4 rounds
     temp ^= keys[4]

     return temp
##### END_QUESTION_2 #####


##### START_QUESTION_3 #####
global s_inv, perm_inv
s_inv = [0]*16
perm_inv = [0]*16

def init_inverse_ops():
      """This function populates  s_inv et perm_inv to make decryption possible.
      Of course, it should be called BEFORE any decryption operation.
      """

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
##### END_QUESTION_3 #####
