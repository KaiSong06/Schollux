import os

from flask import Flask, render_template, request, jsonify
from .geminiWrapper import categorize


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def home():
        return render_template('chat.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        user_message = data.get('message', '')
        
        # Get response from Gemini
        try:
            response = categorize(user_message)
            return jsonify({'response': str(response)})
        except Exception as e:
            return jsonify({'response': f"Error: {str(e)}"}), 500

    return app