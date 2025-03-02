from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GeneratedText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.String(500), nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
