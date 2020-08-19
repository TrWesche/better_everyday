from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, InputRequired


class ScoringSystemParamForm(FlaskForm):
    """Form for creating & updating user goals."""

    score_input = FloatField('Score Input', validators=[InputRequired()])
    score_output = FloatField('Score Output', validators=[InputRequired()])
    name_en = StringField('Special Label', validators=[Length(max=50)])
