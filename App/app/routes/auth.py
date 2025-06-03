from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User, UserRole
from app.extensions import db, login
from werkzeug.security import check_password_hash

# Gestion de l'authentification (login/logout/register)
auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@login.user_loader # Charge l'utilisateur pour Flask-Login
def load_user(uid):
    return User.query.get(int(uid))

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    """Gère la connexion des étudiants/enseignants"""
    if request.method == 'POST':
        # Vérification des identifiants
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.hashed_password, password):
            login_user(user) # Connexion via Flask-Login
            if user.role == UserRole.student:
                # Redirection selon le rôle
                return redirect(url_for('student.tp_page'))
            elif user.role == UserRole.teacher:
                return redirect(url_for('teacher.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash("E-mail ou mot de passe incorrect.", "danger")
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required # Sécurise la route
def logout():
    logout_user()  # Déconnexion
    flash('Déconnecté', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    """Inscription des étudiants"""
    if request.method=='POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash('Email déjà utilisé', 'warning')
        else:
            # Création du compte étudiant
            u = User(
                email=request.form['email'],
                name=request.form['name'],
                password=request.form['password'],
                role=UserRole.student
            )
            db.session.add(u); db.session.commit()
            flash('Compte créé', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')
