from flask import Blueprint, redirect, request,  render_template, flash, url_for
from flask_login import login_required, current_user
from app.models import Cohort, User, UserRole
from app.extensions import db
import random, string

teacher_bp = Blueprint('teacher', __name__, template_folder='../templates/teacher')

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name!='teacher':
        return redirect(url_for('auth.login'))
    cohorts = Cohort.query.all()
    return render_template('dashboard.html', cohorts=cohorts)

# Liste des enseignants
@teacher_bp.route('/admins')
@login_required
def list_admins():
    if getattr(current_user, 'role', None) != UserRole.teacher:
        flash("Accès refusé.", "danger")
        return redirect(url_for('teacher.dashboard'))
    admins = User.query.filter_by(role=UserRole.teacher).all()
    return render_template('teacher/admins_list.html', admins=admins)
    
# Ajout d’un enseignant (affiche le formulaire)
@teacher_bp.route('/admins/add', methods=['GET', 'POST'])
@login_required
def add_admin():
    if getattr(current_user, 'role', None) != UserRole.teacher:
        flash("Accès refusé.", "danger")
        return redirect(url_for('teacher.list_admins'))

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        name  = request.form['name'].strip()

        # Génère un mot de passe aléatoire
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Vérifie l’unicité de l’email
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Erreur : Un enseignant avec cet email existe déjà.", "danger")
            return redirect(url_for('teacher.list_admins'))

        from werkzeug.security import generate_password_hash
        enseignant = User(
            email=email,
            name=name,
            hashed_password=generate_password_hash(password),
            role=UserRole.teacher
        )
        db.session.add(enseignant)
        db.session.commit()
        flash(f"Nouvel enseignant ajouté : {email} (mot de passe provisoire : {password})", "success")
        return redirect(url_for('teacher.list_admins'))

    # GET : juste le formulaire d'ajout
    return render_template('teacher/add_admin.html')

    
# Supprimer un admin
@teacher_bp.route('/admins/delete/<int:admin_id>', methods=['POST'])
@login_required
def delete_admin(admin_id):
    if getattr(current_user, 'role', None) != UserRole.teacher:
        flash("Accès refusé.", "danger")
        return redirect(url_for('teacher.list_admins'))
    admin = User.query.get_or_404(admin_id)
    if admin.id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte enseignant.", "danger")
    else:
        db.session.delete(admin)
        db.session.commit()
        flash(f"Enseignant {admin.email} supprimé avec succès.", "success")
    return redirect(url_for('teacher.list_admins'))
    


