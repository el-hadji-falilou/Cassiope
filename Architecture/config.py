
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CRYPTO_FOLDER = os.getenv('CRYPTO_FOLDER', os.path.join(BASE_DIR, 'crypto-materials'))
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUBMISSIONS_FOLDER = os.getenv('SUBMISSIONS_FOLDER', './submissions')
    CRYPTO_FOLDER      = os.getenv('CRYPTO_FOLDER', './crypto-materials')
    N_PAIRS            = int(os.getenv('N_PAIRS', 2000))
    CRYPTO_FOLDER = os.getenv('CRYPTO_FOLDER', os.path.join(BASE_DIR, 'crypto-materials'))

        # Par défaut, on s’attend à trouver minicipher-main.py à la racine
    MINICIPHER_CMD = os.getenv(
    'MINICIPHER_CMD',
    os.path.abspath('tests/part1/minicipher-main.py'))

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False
