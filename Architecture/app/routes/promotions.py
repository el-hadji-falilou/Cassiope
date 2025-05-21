import os, re, shutil
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Cohort, CryptoMaterial, User, UserRole
from werkzeug.security import generate_password_hash
from app.utils.promotion_utils import generate_diff_material, generate_plaintext_ciphertext, generate_message_xyz,generate_diff_material 
import random, string

passwords = []

promo_bp = Blueprint(
    'admin_promotions',
    __name__,
    url_prefix='/admin/promotions',
    template_folder='../templates/teacher/promotions'
)

@promo_bp.route('/', methods=['GET'])
@login_required
def list_promotions():
    cohorts = Cohort.query.all()
    return render_template('list.html', cohorts=cohorts)

@promo_bp.route('/<int:pid>/set_message', methods=['POST'])
@login_required
def set_message(pid):
    promo = Cohort.query.get_or_404(pid)
    plaintext = request.form['plaintext_msg']

    # Générer message.xyz (en mode CBC, IV=0000)
    msg_meta = generate_message_xyz(
        promo_name = promo.name,
        key_hex    = promo.key_master,
        base_folder= current_app.config['CRYPTO_FOLDER'],
        plaintext  = plaintext
    )

    # Enregistrer en base (ou remplacer l'ancien fichier)
    mat = CryptoMaterial.query.filter_by(
        cohort_id=promo.id, filename=msg_meta['filename']).first()
    if not mat:
        db.session.add(CryptoMaterial(
            cohort    = promo,
            filename  = msg_meta['filename'],
            delta_in  = None,
            delta_out = None
        ))
    db.session.commit()
    flash("Message chiffré et disponible pour les étudiants.", "success")
    return redirect(url_for('admin_promotions.detail_promotion', pid=pid))

@promo_bp.route('/new', methods=['GET','POST'])
@login_required
def new_promotion():
    if request.method == 'POST':
        c = Cohort(
            name=request.form['name'],
            key_master=request.form['key_master']
        )
        db.session.add(c)
        db.session.commit()
        flash('Promotion créée', 'success')
        return redirect(url_for('admin_promotions.list_promotions'))
    return render_template('form.html')

@promo_bp.route('/<int:pid>/download/<filename>')
@login_required
def download_material(pid, filename):
    promo = Cohort.query.get_or_404(pid)
    folder = os.path.join(current_app.config['CRYPTO_FOLDER'], promo.name)
    # Optionnel : contrôler si l’utilisateur a le droit de télécharger
    return send_from_directory(folder, filename, as_attachment=True)


@promo_bp.route('/add_teacher', methods=['POST'])
@login_required
def add_teacher():
    # Optionnel : vérifier que l’utilisateur courant est bien admin
    email = request.form['email']
    name  = request.form['name']
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    user = User(
        email=email,
        name=name,
        hashed_password=generate_password_hash(password),
        role=UserRole.teacher  # ou admin
    )
    db.session.add(user)
    db.session.commit()
    # Optionnel : envoyer un mail au nouvel enseignant (voir plus haut)
    flash(f"Nouvel enseignant ajouté : {email} (mot de passe provisoire : {password})", "success")
    return redirect(url_for('teacher.dashboard'))

@promo_bp.route('/<int:pid>', methods=['GET'])
@login_required
def detail_promotion(pid):
    """
    Affiche le détail de la promotion (clé, formulaire d'upload,
    et liste du matériel déjà importé).
    """
    c = Cohort.query.get_or_404(pid)
    return render_template('detail.html', cohort=c)

@promo_bp.route('/<int:pid>/upload', methods=['POST'])
@login_required
def upload_material(pid):
    c = Cohort.query.get_or_404(pid)
    dest = os.path.join(current_app.config['CRYPTO_FOLDER'], c.name)
    os.makedirs(dest, exist_ok=True)
    for f in request.files.getlist('files'):
        fn = secure_filename(f.filename)
        f.save(os.path.join(dest, fn))
        m = re.search(r'delta_in_([0-9a-f]{4})_([0-9a-f]{4})', fn)
        di, do = (m.group(1), m.group(2)) if m else (None, None)
        db.session.add(CryptoMaterial(
            cohort=c, filename=fn,
            delta_in=di, delta_out=do
        ))
    db.session.commit()
    flash('Matériel importé manuellement.', 'success')
    return redirect(url_for('admin_promotions.detail_promotion', pid=pid))

@promo_bp.route('/<int:pid>/generate', methods=['POST'])
@login_required
def generate_material(pid):
    promo = Cohort.query.get_or_404(pid)
    # purge ancien matériel
    CryptoMaterial.query.filter_by(cohort_id=pid).delete()
    db.session.commit()

    metas = generate_diff_material(
        promo_name  = promo.name,
        key_hex     = promo.key_master,
        count       = current_app.config['N_PAIRS'],
        base_folder = current_app.config['CRYPTO_FOLDER']
    )
    for m in metas:
        db.session.add(CryptoMaterial(
            cohort    = promo,
            filename  = m['filename'],
            delta_in  = m['delta_in'],
            delta_out = m['delta_out']
        ))

    plain_ciph = generate_plaintext_ciphertext(
        promo.name,
        promo.key_master,
        current_app.config['CRYPTO_FOLDER'])

    db.session.add(CryptoMaterial(
        cohort    = promo,
        filename  = plain_ciph['filename'],
        delta_in  = None,
        delta_out = None))

    db.session.commit()
    flash("Matériel différentiel généré avec succès.", "success")
    return redirect(url_for('admin_promotions.detail_promotion', pid=pid))

@promo_bp.route('/<int:pid>/clear', methods=['POST'])
@login_required
def clear_material(pid):
    """
    Supprime de la base et du disque tout le matériel différentiel de la promo.
    """
    promo = Cohort.query.get_or_404(pid)
    # 1) Supprimer les entrées en base
    CryptoMaterial.query.filter_by(cohort_id=pid).delete()
    db.session.commit()

    # 2) Supprimer le dossier sur le disque
    folder = os.path.join(current_app.config['CRYPTO_FOLDER'], promo.name)
    if os.path.isdir(folder):
        shutil.rmtree(folder)

    flash("Tout le matériel différentiel a été supprimé.", "info")
    return redirect(url_for('admin_promotions.detail_promotion', pid=pid))


@promo_bp.route('/<int:pid>/users', methods=['POST'])
@login_required
def add_student(pid):
    """Inscrire un étudiant dans la promo."""
    c = Cohort.query.get_or_404(pid)
    email = request.form['email']
    name  = request.form['name']
    pwd   = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    hashed_password = generate_password_hash(password)
    u = User(
        email        = email,
        name         = name,
        hashed_password=generate_password_hash(password),
        role         = UserRole.student,
        cohort_id    = pid
    )
    db.session.add(u)
    db.session.commit()
    # Ajoute (nom, mail, mdp) à la liste pour affichage
    passwords.append({'name': name, 'email': email, 'password': password})
    # Passe la liste à la page de la promo
    flash(f"Étudiant ajouté : {name} — Mot de passe provisoire : {password}", "info")
    return redirect(url_for('admin_promotions.detail_promotion', pid=pid))

# -------------- SUPPRESSION ----------------
@promo_bp.route('/<int:pid>/delete', methods=['POST'])
@login_required
def delete_promotion(pid):
    """Supprime une promotion et tout son matériel et ses étudiants."""
    c = Cohort.query.get_or_404(pid)
    db.session.delete(c)
    db.session.commit()
    flash(f'Promotion "{c.name}" supprimée.', 'info')
    return redirect(url_for('admin_promotions.list_promotions'))

@promo_bp.route('/<int:pid>/users/<int:uid>/delete', methods=['POST'])
@login_required
def delete_student(pid, uid):
    """Supprime un étudiant de la promotion."""
    u = User.query.filter_by(id=uid, cohort_id=pid).first_or_404()
    db.session.delete(u)
    db.session.commit()
    flash(f'Étudiant "{u.name}" supprimé.', 'info')
    return redirect(url_for('admin_promotions.detail_promotion', pid=pid))