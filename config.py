"""
initializes configurations. import into app.py and call. 
"""

import os 

from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from blueprints.login import login_manager
from model.model import db


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['URI']
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def init_app(app):
    app.config.from_object(Config)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = "You need to be logged in"
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"
    login_manager.use_session_for_next = True
    login_manager.init_app(app)
    migrate = Migrate()
    csrf  = CSRFProtect()
    #init objects with app context
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    import logging
    logging.basicConfig(level=logging.DEBUG)

    return app