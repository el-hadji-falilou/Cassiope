import os
import re
import sys
import subprocess
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="web/templates")

MINICIPHER_PATH = os.path.abspath("submissions/minicipher.py")
COMPUTE_PROBAS_PATH = os.path.abspath("submissions/compute_proba.py")
FIND_KEY = os.path.abspath("submissions/find_key.py")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_code/<int:question_id>", methods=["POST"])
def submit_code(question_id):
    if "code" not in request.files:
        return jsonify({"error": "No file received"}), 400

    file = request.files["code"]
    if file.filename == "":
        return jsonify({"error": "Invalid filename"}), 400

    new_code = file.read().decode('utf-8')

    update_status = update_file(question_id, new_code)

    if not update_status["success"]:
        return jsonify({
            "error": "Failed to update source file",
            "details": update_status["message"]
        }), 500

    try:
        make_process = subprocess.run(
            ["make", "python"],
            check=True,
            cwd="submissions",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Make failed",
            "details": e.stderr
        }), 500

    return jsonify({
        "message": "Code submitted and tested successfully.",
        "details": update_status["message"],
        "stdout": f"Test exécuté pour la question {question_id} après mise à jour.",
        "stderr": ""
    }), 200

@app.route("/get_probas", methods=["GET"])
def get_probas():
    import compute_proba
    compute_proba.compute_probas()
    return jsonify(compute_proba.probas)

@app.route("/validate_input/<int:question_id>/<string:side>", methods=["POST"])
def validate_input(question_id, side):
    student_data = request.get_json()
    with open("expected_answers.json") as f:
        expected = json.load(f)

    key = f"{question_id}_{side}"
    if key not in expected:
        return jsonify({
            "result": "error",
            "message": "Configuration manquante pour cette question"
        }), 400

    expected_data = expected[key]
    errors = []
    
    # Validation pour la question 5 (tableau)
    if question_id == 5:
        # Vérification des δout
        for i in range(16):
            if student_data['deltaOut'][f'val{i}'] != expected_data['deltaOut'][f'val{i}']:
                errors.append({
                    "type": "deltaOut",
                    "index": i,
                    "expected": expected_data['deltaOut'][f'val{i}'],
                    "provided": student_data['deltaOut'][f'val{i}']
                })
        
        # Vérification des probas
        for i in range(16):
            if student_data['proba'][f'val{i}'] != expected_data['proba'][f'val{i}']:
                errors.append({
                    "type": "proba",
                    "index": i+16,
                    "expected": expected_data['proba'][f'val{i}'],
                    "provided": student_data['proba'][f'val{i}']
                })

        if not errors:
            return jsonify({
                "result": "success",
                "message": "Toutes les valeurs sont correctes!",
                "details": []
            })
        else:
            return jsonify({
                "result": "partial",
                "message": f"{16*2 - len(errors)}/{16*2} valeurs correctes",
                "details": errors
            })
        
    # Validation pour la question 6
    if question_id == 6:
        # Vérification des δout
        for i in range(6):
            if student_data[f'val{i}'] != expected_data[f'val{i}']:
                errors.append({
                    "type": "question-6",
                    "index": i,
                    "expected": expected_data[f'val{i}'],
                    "provided": student_data[f'val{i}']
                })

        if not errors:
            return jsonify({
                "result": "success",
                "message": "Toutes les valeurs sont correctes!",
                "details": []
            })
        else:
            return jsonify({
                "result": "partial",
                "message": "Réponses correctes",
                "details": errors
            })
        
    # Validation pour la question 7
    if question_id == 7:
        # Vérification des δout
        for i in range(6):
            if student_data[f'val{i}'] != expected_data[f'val{i}']:
                errors.append({
                    "type": "question-7",
                    "index": i,
                    "expected": expected_data[f'val{i}'],
                    "provided": student_data[f'val{i}']
                })

        if not errors:
            return jsonify({
                "result": "success",
                "message": "Toutes les valeurs sont correctes!",
                "details": []
            })
        else:
            return jsonify({
                "result": "partial",
                "message": "Réponses correctes",
                "details": errors
            })
        
    # Validation pour la question 10
    if question_id == 10:
        # Vérification des δout
        for i in range(4):
            if student_data[f'val{i}'] != expected_data[f'val{i}']:
                errors.append({
                    "type": "question-10",
                    "index": i,
                    "expected": expected_data[f'val{i}'],
                    "provided": student_data[f'val{i}']
                })

        if not errors:
            return jsonify({
                "result": "success",
                "message": "Toutes les valeurs sont correctes!",
                "details": []
            })
        else:
            return jsonify({
                "result": "partial",
                "message": "Réponses correctes",
                "details": errors
            })
        
    # Validation pour la question 11
    if question_id == 11:
        # Vérification des δout
        for i in range(4):
            if student_data[f'val{i}'] != expected_data[f'val{i}']:
                errors.append({
                    "type": "question-11",
                    "index": i,
                    "expected": expected_data[f'val{i}'],
                    "provided": student_data[f'val{i}']
                })

        if not errors:
            return jsonify({
                "result": "success",
                "message": "Toutes les valeurs sont correctes!",
                "details": []
            })
        else:
            return jsonify({
                "result": "partial",
                "message": "Réponses correctes",
                "details": errors
            })
        
    # Validation pour la question 13
    if question_id == 13:
        # Vérification des δout
        for i in range(3):
            if student_data[f'val{i}'] != expected_data[f'val{i}']:
                errors.append({
                    "type": "question-13",
                    "index": i,
                    "expected": expected_data[f'val{i}'],
                    "provided": student_data[f'val{i}']
                })

        if not errors:
            return jsonify({
                "result": "success",
                "message": "Toutes les valeurs sont correctes!",
                "details": []
            })
        else:
            return jsonify({
                "result": "partial",
                "message": "Réponses correctes",
                "details": errors
            })


def update_file(question_id, new_code):
    markers = {
        1: ("##### START_QUESTION_1 #####", "##### END_QUESTION_1 #####"),
        2: ("##### START_QUESTION_2 #####", "##### END_QUESTION_2 #####"),
        3: ("##### START_QUESTION_3 #####", "##### END_QUESTION_3 #####"),
        4: ("##### START_QUESTION_4 #####", "##### END_QUESTION_4 #####"),
        8: ("##### START_QUESTION_8 #####", "##### END_QUESTION_8 #####"),
        9: ("##### START_QUESTION_9 #####", "##### END_QUESTION_9 #####"),
        12: ("##### START_QUESTION_12 #####", "##### END_QUESTION_12 #####"),
        14: ("##### START_QUESTION_14 #####", "##### END_QUESTION_14 #####"),
        15: ("##### START_QUESTION_15 #####", "##### END_QUESTION_15 #####")
    }

    if question_id in {1, 2, 3}:
        PATH = MINICIPHER_PATH
    elif question_id == 4:
        PATH = COMPUTE_PROBAS_PATH
    elif question_id in {8, 9, 12, 14, 15}:
        PATH = FIND_KEY
    else:
        return {"success": False, "message": "Invalid question ID"}

    with open(PATH, 'r') as f:
        content = f.read()

    start_marker, end_marker = markers[question_id]
    pattern = re.compile(
        rf"{re.escape(start_marker)}(.*?){re.escape(end_marker)}",
        flags=re.DOTALL
    )

    if not pattern.search(content):
        return {"success": False, "message": "Markers not found"}

    replacement = f"{start_marker}\n{new_code.strip()}\n{end_marker}"
    content = pattern.sub(replacement, content)

    with open(PATH, 'w') as f:
        f.write(content)

    return {"success": True, "message": f"Updated code for question {question_id}"}

if __name__ == "__main__":
    app.run(debug=True)
