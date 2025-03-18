import os
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath("../Part_1/Encryption/")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_code/<int:question_id>", methods=["POST"])
def submit_code(question_id):
    if "code" not in request.files:
        return "Aucun fichier reçu", 400

    file = request.files["code"]
    if file.filename == "":
        return "Nom de fichier invalide", 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], "minicipher.py")
    file.save(filepath)

    command_base = [
        "docker", "run", "--rm",
        "-v", f"{UPLOAD_FOLDER}:/app"
    ]

    if question_id == 2:
        command = command_base + ["encryption"]
    elif question_id == 3:
        command = command_base + ["decryption"]
    else:
        return "Question inconnue", 400

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Erreur d'exécution : {e.stderr}"

    return f"<pre>{output}</pre>"

if __name__ == "__main__":
    app.run(debug=True)