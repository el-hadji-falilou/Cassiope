import os, sys, subprocess
from flask import current_app

def encrypt_block(plaintext_hex: str, key_hex: str) -> str:
    cmd_path = current_app.config['MINICIPHER_CMD']
    workdir = os.path.dirname(cmd_path)
    if cmd_path.endswith('.py'):
        cmd = [sys.executable, cmd_path, '-e', '-1', '-k', key_hex]
    else:
        cmd = [cmd_path, '-e', '-1', '-k', key_hex]

    print("CMD:", cmd)
    print("CWD:", workdir)
    print("IN:", plaintext_hex)
    print("KEY:", key_hex)

    proc = subprocess.run(
        cmd,
        input=plaintext_hex,
        text=True,
        capture_output=True,
        check=True,
        cwd=workdir
    )
    print("STDOUT:", proc.stdout)
    print("STDERR:", proc.stderr)
    return proc.stdout.strip()
    


def decrypt_block(ciphertext_hex: str, key_hex: str) -> str:
    """
    Déchiffre un bloc 16 bits en mode -d -1 avec la clé key_hex.
    """
    cmd_path = current_app.config['MINICIPHER_CMD']
    workdir  = os.path.dirname(cmd_path)

    if cmd_path.endswith('.py'):
        cmd = [sys.executable, cmd_path, '-d', '-1', '-k', key_hex]
    else:
        cmd = [cmd_path, '-d', '-1', '-k', key_hex]

    proc = subprocess.run(
        cmd,
        input=ciphertext_hex,
        text=True,
        capture_output=True,
        check=True,
        cwd=workdir
    )
   
    return proc.stdout.strip()

