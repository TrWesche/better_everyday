from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import Length, InputRequired


class ScoringSystemParamForm(FlaskForm):
    """Form for creating & updating user goals."""

    score_input = FloatField('Time Spent (mins) *', validators=[InputRequired()], description='The time spent input which will result in the output Numerical Score (User input while tracking progress).')
    score_output = FloatField('Calculated Score *', validators=[InputRequired()], description='The numerical score which the Time Spent input will result in (Calculated value).')
    name_en = StringField('Text Label', validators=[Length(max=50)], description='An encouraging message or text label (ex. A,B,C,D,F) which will be displayed for this score.')
