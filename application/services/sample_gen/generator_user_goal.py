from application.plan.models.model_goal import Goal
from application.plan.models.model_user_goal import User_Goal

from application import db

def checkGoal(title_en):
    goal_result = Goal.query.filter(Goal.title_en == title_en.lower()).first()

    if goal_result:
        return goal_result.id
    else:
        return 0


def generateGoal(title_en, description_public):
    new_goal = Goal(title_en = title_en.lower(), 
        description_public = description_public)

    db.session.add(new_goal)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate goal")

    return new_goal.id


def generateUserGoal(title_en, description_public, user_id, user_persona_id, scoring_system_id, description_private):
    goal_id = checkGoal(title_en)
    if not goal_id:
        goal_id = generateGoal(title_en, description_public)

    new_user_goal = User_Goal(
        active = True,
        user_id = user_id,
        user_persona_id = user_persona_id,
        scoring_system_id = scoring_system_id,
        goal_id = goal_id,
        description_private = description_private
    )

    db.session.add(new_user_goal)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate user goal")

    return new_user_goal.id


