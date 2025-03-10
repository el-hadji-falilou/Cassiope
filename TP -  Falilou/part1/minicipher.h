#ifndef MINICIPHER_H
#define MINICIPHER_H

void init_inverse_ops ();
int encrypt_round (int input, int key, int do_perm);
int minicipher_encrypt (int plaintext, int keys[]);
int decrypt_round (int input, int key, int do_perm);
int minicipher_decrypt (int ciphertext, int keys[]);

#endif
