import os

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUBMISSIONS_FOLDER = os.getenv('SUBMISSIONS_FOLDER', './submissions')
    CRYPTO_FOLDER      = os.getenv('CRYPTO_FOLDER', './crypto-materials')

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False
