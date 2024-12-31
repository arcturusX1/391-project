from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    FloatField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TimeField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pass1 = PasswordField('Password', validators=[DataRequired(), 
                                                  Length(min=8, max=15,
                                                         message='Password must be between 8 and 15 characters long')])
    pass2 = PasswordField('Confirm Password', validators=[DataRequired(),
                                                          EqualTo('pass1',
                                                                message='Passwords do not match')])
    account_type = SelectField('Account Type', choices=[('user', 'User'), ('vet', 'Vet')], validators=[DataRequired()])

    # guide fields
    nid = StringField('NID Number', validators=[DataRequired()])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')