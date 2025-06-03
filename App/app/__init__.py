import os
from flask import Flask
from .extensions import db, migrate, login, mail
from app.routes.student import student_bp

# IMPORTS DES BLUEPRINTS
from .routes.auth       import auth_bp
from .routes.teacher    import teacher_bp
from .routes.promotions import promo_bp
from .routes.main       import main_bp

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # ensure folders
    os.makedirs(app.config['SUBMISSIONS_FOLDER'], exist_ok=True)
    os.makedirs(app.config['CRYPTO_FOLDER'], exist_ok=True)

   
    # ENREGISTREMENT DES BLUEPRINTS
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,      url_prefix='/auth')
    app.register_blueprint(teacher_bp,   url_prefix='/teacher')
    app.register_blueprint(promo_bp)
    app.register_blueprint(student_bp)

    return app

