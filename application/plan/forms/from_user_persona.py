from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length


# TODO: Integrate with User Profile Page

class UserPersonaFrom(FlaskForm):
    """Form for creating & updating user personas."""

    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(max=500)])
    active = BooleanField('Active', default=True)

