from application.plan.models.model_habit import Habit
from application.plan.models.model_user_habit import User_Habit

from application import db

def checkHabit(title_en):
    habit_result = Habit.query.filter(Habit.title_en == title_en.lower()).first()

    if habit_result:
        return habit_result.id
    else:
        return 0


def generateHabit(title_en, description_public):
    new_habit = Habit(title_en = title_en.lower(), 
        description_public = description_public)

    db.session.add(new_habit)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate habit")

    return new_habit.id


def generateUserHabit(title_en, description_public, user_id, user_persona_id, scoring_system_id, description_private):
    habit_id = checkHabit(title_en)
    if not habit_id:
        habit_id = generateHabit(title_en, description_public)

    new_user_habit = User_Habit(
        active = True,
        user_id = user_id,
        user_persona_id = user_persona_id,
        scoring_system_id = scoring_system_id,
        habit_id = habit_id,
        description_private = description_private
    )

    db.session.add(new_user_habit)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate user habit")

    return new_user_habit.id


