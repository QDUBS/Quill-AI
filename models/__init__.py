from flask_sqlalchemy import SQLAlchemy

# Initialize db instance
db = SQLAlchemy()

# Import and register models 
def init_models():
    from models.user import User
    from models.generated_text import GeneratedText
