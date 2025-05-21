from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User, UserRole
from app.extensions import db, login
from werkzeug.security import check_password_hash


auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.hashed_password, password):
            login_user(user)
            if user.role == UserRole.student:
                return redirect(url_for('student.tp_page'))
            elif user.role == UserRole.teacher:
                return redirect(url_for('teacher.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash("E-mail ou mot de passe incorrect.", "danger")
    return render_template('auth/login.html')

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
