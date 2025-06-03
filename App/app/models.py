from .extensions import db
from datetime import datetime
from flask_login import UserMixin
import enum
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole(enum.Enum):
    student = 'student'
    teacher = 'teacher'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer,   primary_key=True)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    name     = db.Column(db.String(80),  nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    role     = db.Column(db.Enum(UserRole), default=UserRole.student, nullable=False)
    cohort_id = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=True)

    @property
    def password(self):
        raise AttributeError("password is write-only")

    @password.setter
    def password(self, plaintext):
        self.pwd_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return check_password_hash(self.pwd_hash, plaintext)

class Cohort(db.Model):
    __tablename__ = 'promotions'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(64), unique=True, nullable=False)
    key_master = db.Column(db.String(80), nullable=False)
    users      = db.relationship('User', backref='cohort', cascade='all, delete-orphan', lazy='dynamic')
    materials  = db.relationship('CryptoMaterial', back_populates='cohort', cascade='all, delete-orphan')

class CryptoMaterial(db.Model):
    __tablename__ = 'crypto_materials'
    id          = db.Column(db.Integer, primary_key=True)
    cohort_id   = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=False)
    filename    = db.Column(db.String(256), nullable=False)
    delta_in    = db.Column(db.String(64), nullable=True)
    delta_out   = db.Column(db.String(64), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    cohort      = db.relationship('Cohort', back_populates='materials')
    
class ValidatedCode(db.Model):
    __tablename__ = 'validated_codes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    part = db.Column(db.String(32), nullable=False)  # 'decrypt', 'decrypt_round', etc.
    code_text = db.Column(db.Text, nullable=False)
    validated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='validated_codes')

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(10), nullable=False)  # "Q1", "Q2", ...
    status = db.Column(db.String(16), default="pending") # "pending", "done", "failed"
    # ... (timestamp, feedback, etc.)
