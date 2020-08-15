from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField
from wtforms.validators import DataRequired, Length


class GoalScoreForm(FlaskForm):
    """Form for creating & updating user goal scores."""

    date = DateField('Date', format='%m/%d/%Y', validators=[DataRequired()])
    score = FloatField('Score', validators=[DataRequired()])
