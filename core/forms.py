import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from core.models import User

def SimpleEmail(message=None):
    def _simple_email(form, field):
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', field.data):
            raise ValidationError(message or 'Invalid email address.')
    return _simple_email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), SimpleEmail()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), SimpleEmail()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    referral_code = StringField('Referral Code (optional)')
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
