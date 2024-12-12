'''# models/agent.py
from models import db
from sqlalchemy.orm import relationship

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    picture_url = db.Column(db.String(255), nullable=True)
    prompt = db.Column(db.Text, nullable=False)

    # Relationship to Chatbot
    chatbots = relationship('Chatbot', backref='agent', lazy=True)

    def __repr__(self):
        return f'<Agent {self.name}>'
'''

from models import db
# Agent Model
class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text)
    prompt = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbots.id'), unique=True, nullable=True)  # Foreign key to Chatbot
