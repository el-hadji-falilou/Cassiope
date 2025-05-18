import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Cohort, CryptoMaterial
from app.models     import User, UserRole
from werkzeug.security import generate_password_hash

import random, string

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
        path = os.path.join(dest, fn)
        f.save(path)

        m = re.search(r'delta_in_([0-9a-f]{4})_([0-9a-f]{4})', fn)
        di, do = (m.group(1), m.group(2)) if m else (None, None)

        mat = CryptoMaterial(
            cohort=c,
            filename=fn,
            delta_in=di,
            delta_out=do
        )
        db.session.add(mat)

    db.session.commit()
    flash('Matériel importé', 'success')
    return redirect(url_for('admin_promotions.detail_promotion', pid=pid))
@promo_bp.route('/<int:pid>/users', methods=['POST'])
@login_required
def add_student(pid):
    """Inscrire un nouvel étudiant dans la promo."""
    c = Cohort.query.get_or_404(pid)
    email = request.form['email']
    name  = request.form['name']
    # mot de passe temporaire aléatoire
    pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    hashed = generate_password_hash(pwd)

    u = User(
       email=email,
       name=name,
       pwd_hash=hashed,
       role=UserRole.student,
       cohort=c
    )
    db.session.add(u)
    db.session.commit()
    flash(f'Étudiant {name} créé ({email}), mot de passe : {pwd}', 'success')
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