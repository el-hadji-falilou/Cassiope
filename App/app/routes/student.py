# app/routes/student.py
from flask import Blueprint, request, jsonify, render_template, current_app, send_from_directory, abort
from flask_login import login_required, current_user
import os
import re
import subprocess
import json
import shutil
import importlib.util

from app.models import Cohort, CryptoMaterial, UserRole

student_bp = Blueprint('student', __name__, template_folder="../templates/student")

MINICIPHER_PATH = os.path.abspath("./app/submissions/minicipher.py")
COMPUTE_PROBAS_PATH = os.path.abspath("./app/submissions/compute_proba.py")
FIND_KEY = os.path.abspath("./app/submissions/find_key.py")
EXPECTED_ANSWER_PATH = os.path.abspath("./app/tests/expected_answers.json")

# Routes existantes
@student_bp.route('/tp')
@login_required
def tp_page():
    if not hasattr(current_user, "role") or current_user.role != UserRole.student:
        abort(403)
    promo = current_user.cohort
    materials = promo.materials if hasattr(promo, 'materials') else []
    return render_template("student/tp_student.html", cohort=promo, materials=materials, user=current_user)

@student_bp.route('/tp/download/<filename>')
@login_required
def download_material(filename):
    promo = current_user.cohort
    folder = os.path.join(current_app.config['CRYPTO_FOLDER'], promo.name)
    safe_files = [m.filename for m in promo.materials]
    if filename not in safe_files:
        abort(403)
    return send_from_directory(folder, filename, as_attachment=True)

@student_bp.route("/submit_code/<int:question_id>", methods=["POST"])
@login_required
def submit_code(question_id):
    print(f"[DEBUG] Handling submission for question {question_id}")

    if "code" not in request.files:
        print("[DEBUG] No code in request.files")
        return jsonify({"error": "No file received"}), 400

    file = request.files["code"]
    print(f"[DEBUG] Received file: {file.filename}")

    if file.filename == "":
        return jsonify({"error": "Invalid filename"}), 400

    new_code = file.read().decode('utf-8')
    print(f"[DEBUG] New code content:\n{new_code[:200]}...")

    update_status = update_file(question_id, new_code)
    print(f"[DEBUG] update_status = {update_status}")

    if not update_status["success"]:
        return jsonify({
            "error": "Failed to update source file",
            "details": update_status["message"]
        }), 500

    make_process = subprocess.run(
        ["make", "python"],
        check=True,
        cwd=current_app.config['SUBMISSIONS_FOLDER'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"[DEBUG] Make output:\n{make_process.stdout}")

    if question_id == 1:
        print("[DEBUG] Running Docker for Q1")

        required_files = [
            ('minicipher', 'minicipher'),
            ('minicipher.py', 'minicipher.py'),
            ('minicipher-main.py', 'minicipher-main.py')
        ]

        for src, dest in required_files:
            src_path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], src)
            dest_path = os.path.join(current_app.config['TEST_ENCRYPTION_FOLDER'], dest)
            print(f"[DEBUG] Copying from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

        build_result = subprocess.run(
            ["docker", "build", "-t", "minicipher-test-encryption", "."],
            cwd=current_app.config['TEST_ENCRYPTION_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[DEBUG] Docker build output:\n{build_result.stdout}")

        if build_result.returncode != 0:
            return jsonify({
                "status": "FAILED",
                "message": "Docker build failed",
                "details": build_result.stderr
            })

        test_result = subprocess.run(
            ["docker", "run", "--rm", "minicipher-test-encryption"],
            cwd=current_app.config['TEST_ENCRYPTION_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        test_passed = "SUCCESS" in test_result.stdout
        print(f"[DEBUG] Docker run output:\n{test_passed}")
        return jsonify({
            "status": "SUCCESS" if test_passed else "FAILED",
            "message": "Test submitted and executed",
            "result": "SUCCESS" if test_passed else "FAILED",
            "details": test_result.stdout
        })

    if question_id == 2:
        print("[DEBUG] Running Docker for Q2")

        required_files = [
            ('minicipher', 'minicipher'),
            ('minicipher.py', 'minicipher.py'),
            ('minicipher-main.py', 'minicipher-main.py')
        ]

        for src, dest in required_files:
            src_path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], src)
            dest_path = os.path.join(current_app.config['TEST_DECRYPTION_FOLDER'], dest)
            print(f"[DEBUG] Copying from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

        build_result = subprocess.run(
            ["docker", "build", "-t", "minicipher-test-decryption", "."],
            cwd=current_app.config['TEST_DECRYPTION_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[DEBUG] Docker build output:\n{build_result.stdout}")

        if build_result.returncode != 0:
            return jsonify({
                "status": "FAILED",
                "message": "Docker build failed",
                "details": build_result.stderr
            })

        test_result = subprocess.run(
            ["docker", "run", "--rm", "minicipher-test-decryption"],
            cwd=current_app.config['TEST_DECRYPTION_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        test_passed = "SUCCESS" in test_result.stdout
        print(f"[DEBUG] Docker run output:\n{test_passed}")
        return jsonify({
            "status": "SUCCESS" if test_passed else "FAILED",
            "message": "Test submitted and executed",
            "result": "SUCCESS" if test_passed else "FAILED",
            "details": test_result.stdout
        })
    
    if question_id == 8:
        print("[DEBUG] Running Docker for Q8")

        required_files = [
            ('find_key.py', 'find_key.py')
        ]

        for src, dest in required_files:
            src_path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], src)
            dest_path = os.path.join(current_app.config['TEST_K5_1_FOLDER'], dest)
            print(f"[DEBUG] Copying from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

        build_result = subprocess.run(
            ["docker", "build", "-t", "find_k5_1", "."],
            cwd=current_app.config['TEST_K5_1_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[DEBUG] Docker build output:\n{build_result.stdout}")

        if build_result.returncode != 0:
            return jsonify({
                "status": "FAILED",
                "message": "Docker build failed",
                "details": build_result.stderr
            })

        test_result = subprocess.run(
            ["docker", "run", "--rm", "find_k5_1"],
            cwd=current_app.config['TEST_K5_1_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        test_passed = "SUCCESS" in test_result.stdout
        print(f"[DEBUG] Docker run output:\n{test_passed}")
        return jsonify({
            "status": "SUCCESS" if test_passed else "FAILED",
            "message": "Test submitted and executed",
            "result": "SUCCESS" if test_passed else "FAILED",
            "details": test_result.stdout
        })
    
    if question_id == 9:
        print("[DEBUG] Running Docker for Q9")

        required_files = [
            ('find_key.py', 'find_key.py')
        ]

        for src, dest in required_files:
            src_path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], src)
            dest_path = os.path.join(current_app.config['TEST_K5_2_FOLDER'], dest)
            print(f"[DEBUG] Copying from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

        build_result = subprocess.run(
            ["docker", "build", "-t", "find_k5_2", "."],
            cwd=current_app.config['TEST_K5_2_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[DEBUG] Docker build output:\n{build_result.stdout}")

        if build_result.returncode != 0:
            return jsonify({
                "status": "FAILED",
                "message": "Docker build failed",
                "details": build_result.stderr
            })

        test_result = subprocess.run(
            ["docker", "run", "--rm", "find_k5_2"],
            cwd=current_app.config['TEST_K5_2_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        test_passed = "SUCCESS" in test_result.stdout
        print(f"[DEBUG] Docker run output:\n{test_passed}")
        return jsonify({
            "status": "SUCCESS" if test_passed else "FAILED",
            "message": "Test submitted and executed",
            "result": "SUCCESS" if test_passed else "FAILED",
            "details": test_result.stdout
        })
    
    if question_id == 12:
        print("[DEBUG] Running Docker for Q12")

        required_files = [
            ('find_key.py', 'find_key.py')
        ]

        for src, dest in required_files:
            src_path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], src)
            dest_path = os.path.join(current_app.config['TEST_K4_FOLDER'], dest)
            print(f"[DEBUG] Copying from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

        build_result = subprocess.run(
            ["docker", "build", "-t", "find_k4", "."],
            cwd=current_app.config['TEST_K4_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[DEBUG] Docker build output:\n{build_result.stdout}")

        if build_result.returncode != 0:
            return jsonify({
                "status": "FAILED",
                "message": "Docker build failed",
                "details": build_result.stderr
            })

        test_result = subprocess.run(
            ["docker", "run", "--rm", "find_k4"],
            cwd=current_app.config['TEST_K4_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        test_passed = "SUCCESS" in test_result.stdout
        print(f"[DEBUG] Docker run output:\n{test_passed}")
        return jsonify({
            "status": "SUCCESS" if test_passed else "FAILED",
            "message": "Test submitted and executed",
            "result": "SUCCESS" if test_passed else "FAILED",
            "details": test_result.stdout
        })
    
    if question_id == 14:
        print("[DEBUG] Running Docker for Q14")

        required_files = [
            ('find_key.py', 'find_key.py')
        ]

        for src, dest in required_files:
            src_path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], src)
            dest_path = os.path.join(current_app.config['TEST_K3_FOLDER'], dest)
            print(f"[DEBUG] Copying from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

        build_result = subprocess.run(
            ["docker", "build", "-t", "find_k3", "."],
            cwd=current_app.config['TEST_K3_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[DEBUG] Docker build output:\n{build_result.stdout}")

        if build_result.returncode != 0:
            return jsonify({
                "status": "FAILED",
                "message": "Docker build failed",
                "details": build_result.stderr
            })

        test_result = subprocess.run(
            ["docker", "run", "--rm", "find_k3"],
            cwd=current_app.config['TEST_K3_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        test_passed = "SUCCESS" in test_result.stdout
        print(f"[DEBUG] Docker run output:\n{test_passed}")
        return jsonify({
            "status": "SUCCESS" if test_passed else "FAILED",
            "message": "Test submitted and executed",
            "result": "SUCCESS" if test_passed else "FAILED",
            "details": test_result.stdout
        })
    
    if question_id == 15:
        print("[DEBUG] Running Docker for Q15")

        required_files = [
            ('find_key.py', 'find_key.py')
        ]

        for src, dest in required_files:
            src_path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], src)
            dest_path = os.path.join(current_app.config['TEST_K1_K2_FOLDER'], dest)
            print(f"[DEBUG] Copying from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

        build_result = subprocess.run(
            ["docker", "build", "-t", "find_k1_k2", "."],
            cwd=current_app.config['TEST_K1_K2_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[DEBUG] Docker build output:\n{build_result.stdout}")

        if build_result.returncode != 0:
            return jsonify({
                "status": "FAILED",
                "message": "Docker build failed",
                "details": build_result.stderr
            })

        test_result = subprocess.run(
            ["docker", "run", "--rm", "find_k1_k2"],
            cwd=current_app.config['TEST_K1_K2_FOLDER'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        test_passed = "SUCCESS" in test_result.stdout
        print(f"[DEBUG] Docker run output:\n{test_passed}")
        return jsonify({
            "status": "SUCCESS" if test_passed else "FAILED",
            "message": "Test submitted and executed",
            "result": "SUCCESS" if test_passed else "FAILED",
            "details": test_result.stdout
        })

    return jsonify({
        "status": "SUCCESS",
        "message": "Test submitted"
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

    if question_id in {1, 2}:
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

@student_bp.route("/get_probas", methods=["GET"])
@login_required
def get_probas():
    path = os.path.join(current_app.config['SUBMISSIONS_FOLDER'], "compute_proba.py")
    spec = importlib.util.spec_from_file_location("compute_proba", path)
    compute_proba = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compute_proba)
    compute_proba.compute_probas()
    return jsonify(compute_proba.probas)

@student_bp.route("/validate_input/<int:question_id>/<string:side>", methods=["POST"])
@login_required
def validate_input(question_id, side):
    student_data = request.get_json()
    with open(EXPECTED_ANSWER_PATH) as f:
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
                    "index": i,
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
