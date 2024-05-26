# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_dropzone import Dropzone
from flask_cors import CORS

from flask_cdn import CDN

db = SQLAlchemy()
login_manager = LoginManager()
cdn = CDN()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):

    # Read debug flag
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')

    # Contextual
    static_prefix = '/static' if DEBUG else '/'

    app = Flask(__name__,static_url_path=static_prefix)
    
    # dropzone for analyzer page
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_MAX_FILE_SIZE=5000,
    DROPZONE_ALLOWED_FILE_TYPE='.exe, .pdf, .txt, .pcap, .pcapng, .jpg, .jpeg, .png, .*',
    DROPZONE_MAX_FILES=30,
    DROPZONE_PARALLEL_UPLOADS=3,  # set parallel amount
    DROPZONE_UPLOAD_MULTIPLE=True,  # enable upload multiple
    )

    cors = CORS(app)
    dropzone = Dropzone(app)

    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    if not DEBUG and 'CDN_DOMAIN' in app.config:
        cdn.init_app(app)

    return app
