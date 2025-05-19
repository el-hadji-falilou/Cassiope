import os, random, subprocess, sys
from app.utils.crypto_utils import encrypt_block
from flask import current_app


DIFFERENTIAL_PATHS = [
    {'step':5, 'delta_in':'0b00', 'delta_out':'0606'},
    {'step':5, 'delta_in':'000d','delta_out':'a0a0'},
    {'step':4, 'delta_in':'0040','delta_out':'0606'},
    {'step':4, 'delta_in':'0005','delta_out':'a0a0'},
    {'step':3, 'delta_in':'0220','delta_out':'0606'},
    {'step':3, 'delta_in':'1010','delta_out':'a0a0'},
    {'step':2, 'delta_in':'bbbb', 'delta_out':None},
]

def generate_diff_material(promo_name: str, key_hex: str, count: int, base_folder: str):
    """
    Génère pour chaque chemin differential `count` paires (C, C'), écrit
    dans base_folder/promo_name/pairs-k{step}_delta_in[_delta_out].txt.
    Retourne liste de metas: filename, delta_in, delta_out.
    """
    out_dir = os.path.join(base_folder, promo_name)
    os.makedirs(out_dir, exist_ok=True)
    metas = []

    for p in DIFFERENTIAL_PATHS:
        fname = f"pairs-k{p['step']}_{p['delta_in']}"
        if p['delta_out']:
            fname += f"_{p['delta_out']}"
        fname += ".txt"
        
        path = os.path.join(out_dir, fname)
        with open(path, 'w') as f:
            for _ in range(count):
                m1 = f"{random.getrandbits(16):04x}"
                m2 = f"{int(m1,16) ^ int(p['delta_in'],16):04x}"
                print(f"m1={m1}, m2={m2}")
                c1 = encrypt_block(m1, key_hex)
                c2 = encrypt_block(m2, key_hex)
                f.write(f"{c1}, {c2}\n")

        metas.append({
            'filename':  fname,
            'delta_in':  p['delta_in'],
            'delta_out': p['delta_out'],
        })
    return metas

def generate_plaintext_ciphertext(promo_name: str, key_hex: str, base_folder: str):
    out_dir = os.path.join(base_folder, promo_name)
    os.makedirs(out_dir, exist_ok=True)
    fname = "plaintext-ciphertext.txt"
    path = os.path.join(out_dir, fname)
    # Choisir un mot 16 bits aléatoire
    p = f"{random.getrandbits(16):04x}"
    c = encrypt_block(p, key_hex)
    with open(path, "w") as f:
        f.write(f"{p}, {c}\n")
    return {'filename': fname, 'plaintext': p, 'ciphertext': c}

def generate_plaintext_ciphertext(promo_name: str, key_hex: str, base_folder: str):
    """
    Génère un fichier plaintext-ciphertext.txt contenant un couple (P, C)
    avec P mot 16 bits aléatoire, C = E_K(P) avec la clé promo.
    """
    from app.utils.crypto_utils import encrypt_block
    import os, random
    out_dir = os.path.join(base_folder, promo_name)
    os.makedirs(out_dir, exist_ok=True)
    fname = "plaintext-ciphertext.txt"
    path = os.path.join(out_dir, fname)

    # 1. Mot aléatoire 16 bits (4 hex)
    p = f"{random.getrandbits(16):04x}"
    # 2. Chiffrement (en bloc unique)
    c = encrypt_block(p, key_hex)

    # 3. Ecriture dans le fichier, au format attendu : "p, c"
    with open(path, "w") as f:
        f.write(f"{p}, {c}\n")

    return {'filename': fname, 'plaintext': p, 'ciphertext': c}


def generate_message_xyz(promo_name: str, key_hex: str, base_folder: str, plaintext: str):
    import tempfile
    import sys, subprocess
    out_dir = os.path.join(base_folder, promo_name)
    os.makedirs(out_dir, exist_ok=True)
    fname = "message.xyz"
    path = os.path.join(out_dir, fname)
    # Ecrire le message dans un fichier temporaire
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmpf:
        tmpf.write(plaintext)
        tmp_plain = tmpf.name

    cmd_path = current_app.config['MINICIPHER_CMD']
    workdir = os.path.dirname(cmd_path)
    if cmd_path.endswith('.py'):
        cmd = [sys.executable, cmd_path, "-e", "-b", "-M", "-k", key_hex, "-i", "0000"]
    else:
        cmd = [cmd_path, "-e", "-b", "-M", "-k", key_hex, "-i", "0000"]

    with open(tmp_plain, "rb") as fin, open(path, "wb") as fout:
        proc = subprocess.run(
            cmd,
            stdin=fin,
            stdout=fout,
            stderr=subprocess.PIPE,
            check=True,
            cwd=workdir
        )
    os.remove(tmp_plain)
    return {'filename': fname}
