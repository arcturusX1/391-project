"""
initializes configurations. import into app.py and call. 
"""

import os 

from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from model.model import db


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['URI']
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def init_app(app):
    app.config.from_object(Config)
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