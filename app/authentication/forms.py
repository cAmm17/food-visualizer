from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length
from app.models import User
import re


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(10, 64, 'Password must be at least '
                                                                    '10 characters long')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(3, 30, 'Username must be between'
                                                                 ' 3 and 30 characters long')])
    email = StringField('Email', validators=[DataRequired(), Email(),
                                             Length(3, 60, 'Please choose an email between '
                                                           '4 and 60 characters long.')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(10, 64, 'Password must be at least '
                                                                    '10 characters long')])
    password2 = PasswordField('Please Enter Password again', validators=[DataRequired(),
                                                                         EqualTo('password'),
                                                                         Length(10, 64,
                                                                                'Password must be at least '
                                                                                '10 characters long')
                                                                         ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already in use. Please choose another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already has an account associated with it.')

    def validate_password(self, password):
        digit_error = re.search(r"\d", password.data) is None
        upper_error = re.search(r"[A-Z]", password.data) is None
        lower_error = re.search(r"[a-z]", password.data) is None
        special_error = re.search(r"\W", password.data) is None
        if digit_error or upper_error or lower_error or special_error:
            raise ValidationError('Please include at least one upper case letter, one lower case '
                                  'letter,one special character, and one digit in your password')
