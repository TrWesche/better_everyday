from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class UserHabitForm(FlaskForm):
    """Form for creating & updating user personas."""

    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    persona = SelectField('Persona', coerce=int)
    active = BooleanField('Active', default=True)