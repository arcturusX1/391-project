from flask import Blueprint, flash, render_template
from werkzeug.security import generate_password_hash
from blueprints.forms import UserForm
from model.model import User, db

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()  # using flask_wtforms form object from UserForm

    if form.validate_on_submit():
        # Retrieve form data
        username = form.username.data
        email = form.email.data
        passwd = form.pass2.data  # Confirmed password field
        
        # Hash the password
        passwd_hash = generate_password_hash(passwd, method='pbkdf2:sha256', salt_length=5)
        print(f"Password Hash: {passwd_hash}")  # Debugging

        try:
            # Create new user object
            new_user = User(
                username=username,
                email=email,
                passwd_hash=passwd_hash
            )
            # Add and commit user to the database
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'User {username} successfully created!', 'success')
            print(f'User {username} successfully created!')
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of error
            flash('An error occurred while creating the user. Please try again.', 'danger')
            print("Database Error:", e)  # Log the error
    else:
        print("Form validation failed. Errors:", form.errors)

    return render_template('signup.html', form=form)
