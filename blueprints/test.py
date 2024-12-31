from flask import Flask, Blueprint, render_template

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/home')
def test():
    return render_template('test.html')