from routes import resumes, templates, ai
import flask_cors

from flask import Flask


app = Flask(__name__)
flask_cors.CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Welcome to the Resume AI API!"

app.register_blueprint(templates)
app.register_blueprint(resumes)
app.register_blueprint(ai)

if __name__ == '__main__':
    app.run(debug=True)