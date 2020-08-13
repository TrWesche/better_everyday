from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class ScoringSystemForm(FlaskForm):
    """Form for creating & updating user goals."""

    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Length(max=500)])
