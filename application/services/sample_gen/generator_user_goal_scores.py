from application.tracking.models.model_goal_score import Goal_Score

from application import db

from datetime import datetime, timezone, timedelta
from random import randint

def generateUserGoalScores(qty_days, user_goal_id, score_input_low, score_input_high):
    today = datetime.now(timezone.utc)

    for day in range(qty_days):
        score_datetime = today - timedelta(day)

        score = randint(score_input_low, score_input_high)

        goal_score = Goal_Score(
            date = score_datetime,
            score = score,
            goal_id = user_goal_id
        )

        db.session.add(goal_score)

    try:
        db.session.commit()
    except:
        print("Failed to generate goal scores")
    
