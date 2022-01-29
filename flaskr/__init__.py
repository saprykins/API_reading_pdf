#!/usr/bin/env python

"""
Initialization of Flask application Factory
"""

from flask import Flask

# import routes
from flaskr.controller import index_blueprint, upload_file_blueprint
from flaskr.controller import get_file_info_blueprint, get_text_blueprint


def init_app():
    """
    Initialize the /core/ application
    """

    # Create a Flask app object
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(index_blueprint)
    app.register_blueprint(upload_file_blueprint)
    app.register_blueprint(get_file_info_blueprint)
    app.register_blueprint(get_text_blueprint)

    return app
