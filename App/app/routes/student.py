from flask import Blueprint, render_template, send_from_directory, current_app, abort, request, jsonify
from flask_login import login_required, current_user
from app.models import Cohort, CryptoMaterial, UserRole
import os

student_bp = Blueprint('student', __name__, template_folder="../templates/student")

@student_bp.route('/tp')
@login_required
def tp_page():
    # Seuls les étudiants ont accès
    if not hasattr(current_user, "role") or current_user.role != UserRole.student:
        abort(403)
    promo = current_user.cohort
    materials = promo.materials if hasattr(promo, 'materials') else []
    return render_template(
        "student/tp_student.html",
        cohort=promo,
        materials=materials,
        user=current_user
    )

@student_bp.route('/tp/download/<filename>')
@login_required
def download_material(filename):
    promo = current_user.cohort
    folder = os.path.join(current_app.config['CRYPTO_FOLDER'], promo.name)
    # Vérifie que le fichier appartient bien à la promo de l'étudiant
    safe_files = [m.filename for m in promo.materials]
    if filename not in safe_files:
        abort(403)
    return send_from_directory(folder, filename, as_attachment=True)

@student_bp.route('/tp/submit_code', methods=['POST'])
@login_required
def submit_code():
    # Sécurité : seulement pour étudiants
    if getattr(current_user, 'role', None) != 'student':
        return jsonify({'success': False, 'message': 'Non autorisé.'}), 403
    data = request.get_json()
    code = data.get('code', '')
    # TODO : sauvegarder le code, lancer correction automatique, etc.
    # Exemple de feedback
    return jsonify({'success': True, 'message': "Code reçu, correction à venir..."})