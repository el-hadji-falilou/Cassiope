import os
from .crypto_utils import encrypt_block

def generate_pairs(output_path, key_hex, delta_in, count=1000):
    """
    Génère `count` paires (C, C⊕delta) et les écrit ligne par ligne.
    """
    with open(output_path, 'w') as f:
        for i in range(count):
            m = f"{i:04x}"
            m2 = f"{int(m,16)^int(delta_in,16):04x}"
            c1 = encrypt_block(m, key_hex)
            c2 = encrypt_block(m2, key_hex)
            f.write(f"{c1}, {c2}\n")
