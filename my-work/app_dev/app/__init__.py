import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    # Load environment variables from .env file so agents have access to API keys
    load_dotenv()

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')

    from app.routes import bp
    app.register_blueprint(bp)

    return app
