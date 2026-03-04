from app.app import create_app
# import flask_cors

app = create_app()

@app.route('/')
def index():
    return 'Welcome to the Resume Builder API!'


if __name__ == '__main__':
    app.run(debug=True)