'''# models/user.py
from models import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'
'''
from models import db

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Relationships
    messages = db.relationship('Message', backref='user', lazy=True)  # One-to-Many
    agents = db.relationship('Agent', backref='user', lazy=True)  # One-to-Many
