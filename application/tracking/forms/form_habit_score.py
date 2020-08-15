from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField
from wtforms.validators import DataRequired, Length


class HabitScoreForm(FlaskForm):
    """Form for creating & updating user habit scores."""

    date = DateField('Date', format='%m/%d/%Y', validators=[DataRequired()])
    score = FloatField('Score', validators=[DataRequired()])
