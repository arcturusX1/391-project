from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from model.model import db, User
from blueprints.forms import UserForm, LoginForm

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.pass2.data
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('auth_bp.login'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, email=email, passwd_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        flash('Signup successful')
        return redirect(url_for('tours_bp.tours'))
    
    return render_template('signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.passwd_hash, password):
            flash('Invalid username or password')
            return redirect(url_for('auth_bp.login'))
        
        session['user_id'] = user.id
        flash('Login successful')
        return redirect(url_for('tours_bp.tours'))
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect(url_for('tours_bp.tours'))