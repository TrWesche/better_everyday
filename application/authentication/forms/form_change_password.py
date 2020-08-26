from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

# TODO: MVP Not Implemented - Change Passwords

class UserChangePasswordForm(FlaskForm):
    """Form for changing user password."""

    password_old = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
