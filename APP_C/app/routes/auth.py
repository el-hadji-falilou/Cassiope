from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User, UserRole
from app.extensions import db, login

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form['email']).first()
        if u and u.check_password(request.form['password']):
            login_user(u)
            flash('Connecté', 'success')
            return redirect(url_for('teacher.dashboard') if u.role==UserRole.teacher else url_for('auth.login'))
        flash('Identifiants invalides', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnecté', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash('Email déjà utilisé', 'warning')
        else:
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
