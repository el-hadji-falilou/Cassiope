"""
Script autonome pour créer un admin et quelques données de démo.
Usage: python init_db.py
"""
from app import create_app
from app.extensions import db
from app.models import User, UserRole
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            email='admin@example.com',
            name='Administrateur',
            hashed_password=generate_password_hash('adminpass'),   # le mot de passe à donner
            role=UserRole.teacher
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin créé !")
    else:
        print("Admin déjà existant.")
