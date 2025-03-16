import os
import logging
from flask import Flask, render_template, request, jsonify
from .Categorize import categorize
from .search import search_papers
from .summarize import summarize, refineQuery

# Configure logging
logging.basicConfig(level=logging.INFO)

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
        try:
            data = request.json
            if not data or 'message' not in data:
                return jsonify({'response': 'No message provided'}), 400
                
            user_message = data['message']
            logging.info(f"Received message: {user_message}")
            
            response = summarize(user_message)
            logging.info(f"Generated response: {response}")
            
            return jsonify({'response': str(response)})
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logging.error(error_msg)
            return jsonify({'response': error_msg}), 500

    return app