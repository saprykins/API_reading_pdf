#!/usr/bin/env python

"Initialization of Flask application"

# STEPS OF IMPROUVEMENT
# Try to use pprint
# delete "debug=True" in main function
# need to add processing state (to be able to share status)
# tbc number of blueprints
# tbc if can keep app in __init__.py outside function

from flask import Flask
from flaskr.controller import index_blueprint, upload_file_blueprint
from flaskr.controller import get_file_info_blueprint, get_text_blueprint

def init_app():
    """
    Flask factory
    """
    app = Flask(__name__)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(upload_file_blueprint)
    app.register_blueprint(get_file_info_blueprint)
    app.register_blueprint(get_text_blueprint)

    return app
