from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class UserGoalForm(FlaskForm):
    """Form for creating & updating user goals."""

    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    persona = SelectField('Persona', coerce=int)
    scoring_system_id = SelectField('Scoring System', coerce=int, choices=[(1, "Default")])
    schedule_id = SelectField('Schedule', coerce=int, choices=[(1, "Default")])
    active = BooleanField('Active', default=True)