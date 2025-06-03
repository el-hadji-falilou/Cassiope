import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')

    MINICIPHER_CMD = os.path.join(BASE_DIR, 'app', 'submissions', 'minicipher-main.py')
    
    SUBMISSIONS_FOLDER = os.getenv('SUBMISSIONS_FOLDER', './submissions')
    CRYPTO_FOLDER      = os.getenv('CRYPTO_FOLDER', './crypto-materials')
    
    CRYPTO_FOLDER = os.getenv('CRYPTO_FOLDER', os.path.join(BASE_DIR, 'crypto-materials'))
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Path configurations
    CRYPTO_FOLDER = os.path.join(BASE_DIR, 'crypto-materials')
    SUBMISSIONS_FOLDER = os.path.join(BASE_DIR, 'app', 'submissions')
    TEST_ENCRYPTION_FOLDER = os.path.join(BASE_DIR, 'app', 'tests', 'Encryption')
    TEST_DECRYPTION_FOLDER = os.path.join(BASE_DIR, 'app', 'tests', 'Decryption')
    TEST_K5_1_FOLDER = os.path.join(BASE_DIR, 'app', 'tests', 'find_k5_1')
    TEST_K5_2_FOLDER = os.path.join(BASE_DIR, 'app', 'tests', 'find_k5_2')
    TEST_K4_FOLDER = os.path.join(BASE_DIR, 'app', 'tests', 'find_k4')
    TEST_K3_FOLDER = os.path.join(BASE_DIR, 'app', 'tests', 'find_k3')
    TEST_K1_K2_FOLDER = os.path.join(BASE_DIR, 'app', 'tests', 'find_k1_k2')

    # Crypto settings
    N_PAIRS = int(os.getenv('N_PAIRS', 2000))

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
