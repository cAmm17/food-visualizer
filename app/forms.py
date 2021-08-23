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
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(),
                                                      Length(10, 64, 'Password must be at least '
                                                                     '10 characters long')])
    password2 = PasswordField('Please Enter Password again', validators=[DataRequired(),
                                                                         EqualTo(password1),
                                                                         Length(10, 64,
                                                                                'Password must be at least '
                                                                                '10 characters long')
                                                                         ])
    submit = SubmitField('Register')

    def validateUsername(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already in use. Please choose another username.')
        if username.data.length() > 30 or username.data.length() < 3:
            raise ValidationError('Please choose a username between 4 and 30 characters long.')

    def validateEmail(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already has an account associated with it.')
        if email.data.length() > 60 or email.data.length() < 3:
            raise ValidationError('Please choose an email between 4 and 60 characters long.')

    def validatePassword(self, password):
        digit_error = re.search(r"\d", password) is None
        upper_error = re.search(r"[A-Z]", password) is None
        lower_error = re.search(r"[a-z]", password) is None
        special_error = re.search(r"\W", password) is None
        if digit_error or upper_error or lower_error or special_error:
            raise ValidationError('Please include at least one upper case letter, one lower case '
                                  'letter,one special character, and one digit in your password')
