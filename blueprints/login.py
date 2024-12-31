from flask import Blueprint, flash, redirect, render_template, url_for, abort, current_app, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from blueprints.forms import LoginForm, UserForm
from model.model import User
# Define the auth blueprint

auth_bp = Blueprint('auth_bp', __name__)

# Initialize the login manager
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
                          
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwd_hash, password):
            login_user(user, remember=remember)

            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                flash('Login Successful!', 'success')
                return redirect(next_page)
            else:
                print(f'{email} Login Successful!', 'success')
                return redirect(url_for('test_bp.test'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    print('logged out')
    return redirect(url_for('test_bp.test'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
