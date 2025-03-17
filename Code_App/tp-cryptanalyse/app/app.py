from flask import Flask, request, render_template, send_file
import subprocess
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads'  # Dossier pour enregistrer les fichiers soumis
app.config['DOWNLOADS_FOLDER'] = 'downloads'  # Dossier pour les fichiers à télécharger
app.config['REFERENCE_FOLDER'] = 'reference'  # Dossier pour les fichiers de référence

# Créer le dossier uploads s'il n'existe pas
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    # Chemin vers le fichier à télécharger
    file_path = os.path.join(app.config['DOWNLOADS_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

@app.route('/submit_code/<int:question>', methods=['POST'])
def submit_code(question):
    if 'code' not in request.files:
        return "Aucun fichier téléversé", 400

    file = request.files['code']
    if file.filename == '':
        return "Aucun fichier sélectionné", 400

    # Enregistrer le fichier soumis
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Exécuter le script de test
    if question == 2:
        script = "./test-encryption.sh 0"
        reference_file = os.path.join(app.config['REFERENCE_FOLDER'], "test-encryption.0.out")
    elif question == 3:
        script = "./test-decryption.sh 0"
        reference_file = os.path.join(app.config['REFERENCE_FOLDER'], "test-decryption.0.out")
    else:
        return "Question non reconnue", 400

    try:
        # Exécuter le script dans un conteneur Docker
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{os.getcwd()}/app/uploads:/code", "tp-cryptanalyse", script],
            capture_output=True, text=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Erreur lors de l'exécution du code : {e.stderr}"

    # Comparer la sortie avec le fichier de référence
    if compare_files(output, reference_file):
        result_message = "Le code est correct !"
        student_output = None
        expected_output = None
    else:
        result_message = "Le code contient des erreurs."
        # Récupérer les cinq premières lignes de la sortie de l'étudiant
        student_output = "\n".join(output.splitlines()[:5])
        # Récupérer les cinq premières lignes du fichier de référence
        with open(reference_file, 'r') as f:
            expected_output = "\n".join(f.read().splitlines()[:5])

    # Supprimer le fichier après traitement
    os.remove(file_path)

    # Retourner uniquement le feedback
    return render_template('feedback.html', **{
        "result": result_message,
        "student_output": student_output,
        "expected_output": expected_output
    })

def compare_files(output, reference_file):
    with open(reference_file, 'r') as f:
        reference_output = f.read()
    return output.strip() == reference_output.strip()

if __name__ == '__main__':
    app.run(debug=True)