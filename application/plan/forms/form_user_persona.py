from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class UserPersonaForm(FlaskForm):
    """Form for creating & updating user personas."""

    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    active = BooleanField('Active', default=True)

