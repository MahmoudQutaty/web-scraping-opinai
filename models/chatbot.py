'''# models/chatbot.py
from models import db
from sqlalchemy.orm import relationship

class Chatbot(db.Model):
    __tablename__ = 'chatbots'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)

    # Relationship to messages
    messages = relationship('Message', backref='chatbot', lazy=True)

    def __repr__(self):
        return f'<Chatbot {self.name}>'
'''
from models import db

# Chatbot Model
class Chatbot(db.Model):
    __tablename__ = 'chatbots'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    agent = db.relationship('Agent', backref='chatbot', uselist=False)  # One-to-One
