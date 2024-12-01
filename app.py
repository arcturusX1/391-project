from flask import Flask 
from register_bp import register_blueprints
app = Flask(__name__)

register_blueprints(app)

if __name__== "__main__":
    app.run(host='0.0.0.0', debug=True)