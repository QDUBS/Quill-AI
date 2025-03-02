import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models.generated_text import db
from routes.auth import auth
from routes.generated_text import text

# Initialize app
load_dotenv()
app = Flask(__name__)
 
# App config
app.config['DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialise database
db.init_app(app)
jwt = JWTManager(app)

# Register routes
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(text, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
