import os
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')

    from app.routes import bp
    app.register_blueprint(bp)

    return app
