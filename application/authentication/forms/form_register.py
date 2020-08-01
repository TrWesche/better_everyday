from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo


class UserRegisterForm(FlaskForm):
    """Form for registering new users."""

    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=100)])
    

