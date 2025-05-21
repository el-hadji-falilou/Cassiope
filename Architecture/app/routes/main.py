# app/routes/main.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    # Ici vous pouvez récupérer vos questions / steps si besoin,
    # et le matériel crypto via current_user.cohort.materials
    return render_template('index.html')
