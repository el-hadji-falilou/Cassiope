import os
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Répertoire de travail pour Docker et stockage des fichiers
WORKDIR = "/home/endiaye/TSP/2A/Cassiopé/Cassiope/TP-Falilou/part1/test-encryption"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vérification du Code</title>
</head>
<body>
    <h1>Vérification du Code</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Vérifier</button>
    </form>
    <pre>{{ result }}</pre>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(WORKDIR, "minicipher.py")
    file.save(file_path)

    # Exécuter Docker dans WORKDIR
    output = subprocess.run(
        ["docker", "build", "-t", "crypto_test", "."],
        capture_output=True,
        text=True,
        cwd=WORKDIR  # Définit le répertoire de travail
    )
    output = subprocess.run(
        ["docker", "run", "--rm", "-v", f"{WORKDIR}:/app", "crypto_test"],
        capture_output=True,
        text=True,
        cwd=WORKDIR  # Définit le répertoire de travail
    )

    return render_template_string(HTML_TEMPLATE, result=output.stdout)

if __name__ == '__main__':
    app.run(debug=True)