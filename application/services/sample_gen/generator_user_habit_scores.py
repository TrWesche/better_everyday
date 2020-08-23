from application.tracking.models.model_habit_score import Habit_Score

from application import db

from datetime import datetime, timezone, timedelta
from random import randint

def generateUserHabitScores(qty_days, user_habit_id, score_input_low, score_input_high):
    today = datetime.now(timezone.utc)

    for day in range(qty_days):
        score_datetime = today - timedelta(day)

        score = randint(score_input_low, score_input_high)

        habit_score = Habit_Score(
            date = score_datetime,
            score = score,
            habit_id = user_habit_id
        )

        db.session.add(habit_score)

    try:
        db.session.commit()
    except:
        print("Failed to generate habit scores")
    
