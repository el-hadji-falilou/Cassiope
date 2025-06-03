# Initialisation des extensions Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
from flask_login      import LoginManager
from flask_mail       import Mail

# Instances des extensions
db      = SQLAlchemy() # ORM pour la base de données
migrate = Migrate()    # Gestion des migrations
login   = LoginManager() # Gestion d'authentification
login.login_view = 'auth.login' # Vue de login par défaut
mail = Mail()  # Service d'envoi d'emails
