from app.routes import resumes, templates, ai
import flask_cors

from flask import Flask

def create_app():   
    app = Flask(__name__)
    flask_cors.CORS(app)  # Enable CORS for all routes



    app.register_blueprint(templates)
    app.register_blueprint(resumes)
    app.register_blueprint(ai)
    return app