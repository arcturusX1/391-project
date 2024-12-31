from flask import Flask 
from register_bp import register_blueprints
from config import init_app
app = Flask(__name__)

init_app(app)
register_blueprints(app)

if __name__== "__main__":
    app.run(host='0.0.0.0', debug=True)