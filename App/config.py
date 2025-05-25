import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Path configurations
    CRYPTO_FOLDER = os.path.join(BASE_DIR, 'crypto-materials')
    SUBMISSIONS_FOLDER = os.path.join(BASE_DIR, 'app', 'submissions')
    TESTS_FOLDER_Q1 = os.path.join(BASE_DIR, 'app', 'tests', 'Q1')
    TESTS_FOLDER_Q3 = os.path.join(BASE_DIR, 'app', 'tests', 'Q2')
    
    # Crypto settings
    N_PAIRS = int(os.getenv('N_PAIRS', 2000))

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
