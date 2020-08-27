from .generator_scoring_sys import generateScoringSystem
from .generator_user_persona import generateUserPersona
from .generator_user_habit import generateUserHabit
from .generator_user_habit_scores import generateUserHabitScores
from .generator_user_goal import generateUserGoal
from .generator_user_goal_scores import generateUserGoalScores


def generateSampleData(user_id):
    # Sample scoring system is created
    scoring_system_title = "Sample Scoring System"
    scoring_system_description = "Getting you up and running with a sample scoring system.  Feel free to update or delete this to match your preference!"
    scoring_system_param_list = [
        {'score_bp': 0, 'score_input': 0, 'score_output': 0, 'name_en': 'F'},
        {'score_bp': 1, 'score_input': 29, 'score_output': 0, 'name_en': 'F'},
        {'score_bp': 2, 'score_input': 39, 'score_output': 1, 'name_en': 'D'},
        {'score_bp': 3, 'score_input': 49, 'score_output': 2, 'name_en': 'C'},
        {'score_bp': 4, 'score_input': 59, 'score_output': 3, 'name_en': 'B'},
        {'score_bp': 5, 'score_input': 69, 'score_output': 4, 'name_en': 'A'},
    ]

    scoring_system_id = generateScoringSystem(user_id, scoring_system_title, scoring_system_description, scoring_system_param_list)


    # Sample user persona is created
    user_persona_title = "samplepersona"
    user_persona_description_public = "Sample persona public description."
    user_persona_description_private = "We created this sample persona to help you get started!  Feel free to update or delete this to match your preference!"

    user_persona_id = generateUserPersona(user_persona_title, user_persona_description_public, user_id, 
                                            user_persona_description_private)



    # Sample user habit is created
    user_habit_title = "samplehabit"
    user_habit_description_public = "Sample habit public description"
    user_habit_description_private = "We created this sample habit to help you get started!  Feel free to update or delete this to match your preference!"


    user_habit_id = generateUserHabit(user_habit_title, user_habit_description_public, user_id, user_persona_id, 
                                        scoring_system_id, user_habit_description_private)


    # Sample habit scores are generated
    generateUserHabitScores(7, user_habit_id, 20, 80)



    # Sample user goal is created
    user_goal_title = "samplegoal"
    user_goal_description_public = "Sample goal public description"
    user_goal_description_private = "We created this sample goal to help you get started!  Feel free to update or delete this to match your preference!"


    user_goal_id = generateUserGoal(user_goal_title, user_goal_description_public, user_id, user_persona_id, 
                                        scoring_system_id, user_goal_description_private)

    generateUserGoalScores(7, user_goal_id, 20, 80)
