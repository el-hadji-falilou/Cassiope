"""
Script autonome pour créer un admin et quelques données de démo.
Usage: python init_db.py
"""
from app import create_app
from app.extensions import db
from app.models import User, UserRole

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@example.com').first():
        u = User(
            email='admin@example.com',
            name='Admin',
            password='adminpass',  # passera par setter
            role=UserRole.teacher
        )
        db.session.add(u)
        db.session.commit()
        print("Admin créé: admin@example.com / adminpass")
    else:
        print("Admin déjà existant.")
