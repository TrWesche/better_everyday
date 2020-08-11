import os

from application.user.models.model_user import User
from application.authentication.models.model_auth import Authentication

from application.plan.models.model_persona import Persona
from application.plan.models.model_habit import Habit
from application.plan.models.model_goal import Goal

from application.plan.models.model_user_persona import User_Persona
from application.plan.models.model_user_habit import User_Habit
from application.plan.models.model_user_goal import User_Goal

from application.tracking.models.model_scoring_system import Scoring_System
from application.tracking.models.model_reminder_schedule import Reminder_Schedule
from application.tracking.models.model_scoring_system_params import Scoring_System_Params
from application.tracking.models.model_goal_score import Goal_Score
from application.tracking.models.model_habit_score import Habit_Score

from datetime import datetime, timedelta

os.environ['DATABASE_URL'] = "postgres:///better-everyday-test-v2"

from wsgi import app
# from wsgi import app
from application import db

with app.app_context():
    # Password = password
    a1 = Authentication(
        username="testuser1",
        password="$2b$12$gyjYvEBqcebZBKiX3C8OGO5cNiXmNVFdzVbcNdxE/eCruG4I5lEOG"
    )

    a2 = Authentication(
        username="testuser2",
        password="$2b$12$gyjYvEBqcebZBKiX3C8OGO5cNiXmNVFdzVbcNdxE/eCruG4I5lEOG"
    )

    u1 = User(
        id = 1,
        first_name="Test",
        last_name="User",
        email="testuser1@test.com",
        username="testuser1",
        public = True
    )

    u2 = User(
        id = 2,
        first_name="Test",
        last_name="User",
        email="testuser2@test.com",
        username="testuser2",
        public = True
    )

    db.session.add_all([a1, a2])
    db.session.commit()
    db.session.add_all([u1, u2])
    db.session.commit()


    p1 = Persona(
        id = 1,
        title_en = "testpersona1",
        description_public = "ThisIsAPublicDescription Persona 1"
    )

    p2 = Persona(
        id = 2,
        title_en = "testpersona2",
        description_public = "ThisIsAPublicDescription Persona 2"
    )

    p3 = Persona(
        id = 3,
        title_en = "testpersona3",
        description_public = "ThisIsAPublicDescription Persona 3"
    )

    h1 = Habit(
        id = 1,
        title_en = "testhabit1",
        description_public = "ThisIsAPublicDescription Habit 1"
    )

    h2 = Habit(
        id = 2, 
        title_en = "testhabit2",
        description_public = "ThisIsAPublicDescription Habit 2"
    )

    h3 = Habit(
        id = 3,
        title_en = "testhabit3",
        description_public = "ThisIsAPublicDescription Habit 3"
    )

    g1 = Goal(
        id = 1,
        title_en = "testgoal1",
        description_public = "ThisIsAPublicDescription Goal 1"
    )

    g2 = Goal(
        id = 2,
        title_en = "testgoal2",
        description_public = "ThisIsAPublicDescription Goal 2"
    )

    g3 = Goal(
        id = 3,
        title_en = "testgoal3",
        description_public = "ThisIsAPublicDescription Goal 3"
    )


    db.session.add_all([p1, p2, p3, h1, h2, h3, g1, g2, g3])
    db.session.commit()

    score1 = Scoring_System(
        id = 1,
        user_id = 1,
        title_en = "User1 US Grades System 1",
        description = "US Grading System 1",
        public = True
    )

    score2 = Scoring_System(
        id = 2,
        user_id = 1,
        title_en = "User1 Scoring System 2",
        description = "Some Sort of Scoring System 1",
        public = False
    )

    score3 = Scoring_System(
        id = 3,
        user_id = 2,
        title_en = "User2 Scoring System 3",
        description = "Some Sort of Scoring System 3",
        public = False
    )

    score4 = Scoring_System(
        id = 4,
        user_id = 2,
        title_en = "User1 Scoring System 4",
        description = "Some Sort of Scoring System 4",
        public = False
    )

   


    sched1 = Reminder_Schedule(    
        id = 1,
        user_id = 1,
        title_en = "User1 Schedule 1",
        description = "User1 Schedule Description",
        public = True,
        global_time = "1900-01-01 20:00:00-06",
        monday = True,
        tuesday = True,
        wednesday = True,
        thursday = True,
        friday = True,
        saturday = False,
        sunday = False
    )

    sched2 = Reminder_Schedule(    
        id = 2,
        user_id = 2,
        title_en = "User2 Schedule 2",
        description = "User2 Schedule Description",
        public = False,
        global_time = "1900-01-01 20:00:00-06",
        monday = True,
        tuesday = True,
        wednesday = True,
        thursday = True,
        friday = True,
        saturday = False,
        sunday = False
    )

    db.session.add_all([score1, score2, score3, score4, sched1, sched2])
    db.session.commit()


    score1_param_1 = Scoring_System_Params(
        id = 1,
        scoring_system_id = 1,
        score_bp = 0,
        score_input = 0,
        score_output = 0,
        name_en = "F"
    )

    score1_param_2 = Scoring_System_Params(
        id = 2,
        scoring_system_id = 1,
        score_bp = 1,
        score_input = 59,
        score_output = 0,
        name_en = "F"
    )

    score1_param_3 = Scoring_System_Params(
        id = 3,
        scoring_system_id = 1,
        score_bp = 2,
        score_input = 69,
        score_output = 1,
        name_en = "D"
    )

    score1_param_4 = Scoring_System_Params(
        id = 4,
        scoring_system_id = 1,
        score_bp = 3,
        score_input = 79,
        score_output = 2,
        name_en = "C"
    )

    score1_param_5 = Scoring_System_Params(
        id = 5,
        scoring_system_id = 1,
        score_bp = 4,
        score_input = 89,
        score_output = 3,
        name_en = "B"
    )

    score1_param_6 = Scoring_System_Params(
        id = 6,
        scoring_system_id = 1,
        score_bp = 5,
        score_input = 100,
        score_output = 4,
        name_en = "A"
    )

    score2_param_1 = Scoring_System_Params(
        id = 7,
        scoring_system_id = 2,
        score_bp = 0,
        score_input = 0,
        score_output = 0,
        name_en = None
    )

    score2_param_2 = Scoring_System_Params(
        id = 8,
        scoring_system_id = 2,
        score_bp = 1,
        score_input = 50,
        score_output = 2,
        name_en = None
    )

    score2_param_3 = Scoring_System_Params(
        id = 9,
        scoring_system_id = 2,
        score_bp = 2,
        score_input = 100,
        score_output = 5,
        name_en = None
    )

    score3_param_1 = Scoring_System_Params(
        id = 10,
        scoring_system_id = 3,
        score_bp = 0,
        score_input = 0,
        score_output = 0,
        name_en = None
    )

    score3_param_2 = Scoring_System_Params(
        id = 11,
        scoring_system_id = 3,
        score_bp = 1,
        score_input = 10,
        score_output = 1,
        name_en = None
    )

    score3_param_3 = Scoring_System_Params(
        id = 12,
        scoring_system_id = 3,
        score_bp = 2,
        score_input = 60,
        score_output = 5,
        name_en = None
    )

    score3_param_4 = Scoring_System_Params(
        id = 13,
        scoring_system_id = 3,
        score_bp = 3,
        score_input = 90,
        score_output = 10,
        name_en = None
    )

    score4_param_1 = Scoring_System_Params(
        id = 14,
        scoring_system_id = 4,
        score_bp = 0,
        score_input = 0,
        score_output = 0,
        name_en = "You can do better then that!"
    )

    score4_param_2 = Scoring_System_Params(
        id = 15,
        scoring_system_id = 4,
        score_bp = 1,
        score_input = 30,
        score_output = 50,
        name_en = "Just a little more!"
    )

    score4_param_3 = Scoring_System_Params(
        id = 16,
        scoring_system_id = 4,
        score_bp = 2,
        score_input = 60,
        score_output = 100,
        name_en = "Target Achieved!"
    )

    score4_param_4 = Scoring_System_Params(
        id = 17,
        scoring_system_id = 4,
        score_bp = 3,
        score_input = 72,
        score_output = 120,
        name_en = "Going beyond the call of duty!"
    )

    db.session.add_all([score1_param_1, score1_param_2, score1_param_3, score1_param_4, score1_param_5, score1_param_6, score2_param_1, 
                        score2_param_2, score2_param_3, score3_param_1, score3_param_2, score3_param_3, score3_param_4, score4_param_1,
                        score4_param_2, score4_param_3, score4_param_4])
    db.session.commit()



    u1_p1 = User_Persona(
        id = 1,
        active = True,
        user_id = 1,
        persona_id = 1,
        description_private = None
    )

    u1_p2 = User_Persona(
        id = 2,
        active = True,
        user_id = 1,
        persona_id = 2,
        description_private = None
    )

    u1_p3 = User_Persona(
        id = 3,
        active = True,
        user_id = 1,
        persona_id = 3,
        description_private = "This is a private description Persona 3"
    )

    u2_p1 = User_Persona(
        id = 4,
        active = True,
        user_id = 2,
        persona_id = 1,
        description_private = "This is a private description Persona 1"
    )

    u2_p2 = User_Persona(
        id = 5,
        active = True,
        user_id = 2,
        persona_id = 2,
        description_private = "This is a private description Persona 2"
    )

    u2_p3 = User_Persona(
        id = 6,
        active = True,
        user_id = 2,
        persona_id = 3,
        description_private = None
    )

    db.session.add_all([u1_p1, u1_p2, u1_p3, u2_p1, u2_p2, u2_p3])
    db.session.commit()

# One Goal per Persona
    u1_g1 = User_Goal(
        id = 1,
        active = True,
        user_id = 1,
        user_persona_id = 1,
        scoring_system_id = 1,
        schedule_id = 1,
        goal_id = 1,
        description_private = None
    )

    u1_g2 = User_Goal(
        id = 2,
        active = True,
        user_id = 1,
        user_persona_id = 2,
        scoring_system_id = 2,
        schedule_id = 1,
        goal_id = 2,
        description_private = None
    )

    u1_g3 = User_Goal(
        id = 3,
        active = True,
        user_id = 1,
        user_persona_id = 1,
        scoring_system_id = 1,
        schedule_id = 1,
        goal_id = 3,
        description_private = "This is a private description Goal 3"
    )

# One Goal no Persona
    u2_g1 = User_Goal(
        id = 4,
        active = True,
        user_id = 2,
        user_persona_id = None,
        scoring_system_id = 3,
        schedule_id = 2,
        goal_id = 1,
        description_private = "This is a private description Goal 1"
    )

# Mulitple Goals per Persona
    u2_g2 = User_Goal(
        id = 5,
        active = True,
        user_id = 2,
        user_persona_id = 2,
        scoring_system_id = 4,
        schedule_id = 2,
        goal_id = 2,
        description_private = "This is a private description Goal 2"
    )

    u2_g3 = User_Goal(
        id = 6,
        active = True,
        user_id = 2,
        user_persona_id = 2,
        scoring_system_id = 3,
        schedule_id = 2,
        goal_id = 3,
        description_private = None
    )

    db.session.add_all([u1_g1, u1_g2, u1_g3, u2_g1, u2_g2, u2_g3])
    db.session.commit()



# One Habit per Persona
    u1_h1 = User_Habit(
        id = 1,
        active = True,
        user_id = 1,
        user_persona_id = 1,
        scoring_system_id = 1,
        schedule_id = 1,
        habit_id = 1,
        linked_goal_id = None,
        description_private = "This is a private description Habit 1"
    )

    u1_h2 = User_Habit(
        id = 2,
        active = True,
        user_id = 1,
        user_persona_id = 2,
        scoring_system_id = 2,
        schedule_id = 1,
        habit_id = 2,
        linked_goal_id = None,
        description_private = "This is a private description Habit 2"
    )

    u1_h3 = User_Habit(
        id = 3,
        active = True,
        user_id = 1,
        user_persona_id = 1,
        scoring_system_id = 1,
        schedule_id = 1,
        habit_id = 3,
        linked_goal_id = 2,
        description_private = None
    )

# One Habit no Persona
    u2_h1 = User_Habit(
        id = 4,
        active = True,
        user_id = 2,
        user_persona_id = None,
        scoring_system_id = 3,
        schedule_id = 2,
        habit_id = 1,
        linked_goal_id = None,
        description_private = None
    )

# Mulitple Habits per Persona
    u2_h2 = User_Habit(
        id = 5,
        active = True,
        user_id = 2,
        user_persona_id = 2,
        scoring_system_id = 4,
        schedule_id = 2,
        habit_id = 2,
        linked_goal_id = None,
        description_private = None
    )

    u2_h3 = User_Habit(
        id = 6,
        active = True,
        user_id = 2,
        user_persona_id = 2,
        scoring_system_id = 3,
        schedule_id = 2,
        habit_id = 3,
        linked_goal_id = None,
        description_private = "This is a private description Habit 3"
    )

    db.session.add_all([u1_h1, u1_h2, u1_h3, u2_h1, u2_h2, u2_h3])
    db.session.commit()


#  1 week of history
    score1_u1_h1 = Habit_Score(
        id = 1,
        date = "2020-08-03 20:00:00-06",
        score = 50.0,
        habit_id = 1
    )

    score2_u1_h1 = Habit_Score(
        id = 2,
        date = "2020-08-02 20:00:00-06",
        score = 60.0,
        habit_id = 1
    )

    score3_u1_h1 = Habit_Score(
        id = 3,
        date = "2020-08-01 20:00:00-06",
        score = 80.0,
        habit_id = 1
    )

    score4_u1_h1 = Habit_Score(
        id = 4,
        date = "2020-07-31 20:00:00-06",
        score = 65.0,
        habit_id = 1
    )

    score5_u1_h1 = Habit_Score(
        id = 5,
        date = "2020-07-30 20:00:00-06",
        score = 45.0,
        habit_id = 1
    )

    score6_u1_h1 = Habit_Score(
        id = 6,
        date = "2020-07-29 20:00:00-06",
        score = 0.0,
        habit_id = 1
    )

    score7_u1_h1 = Habit_Score(
        id = 7,
        date = "2020-07-28 20:00:00-06",
        score = 90.0,
        habit_id = 1
    )

    db.session.add_all([score1_u1_h1, score2_u1_h1, score3_u1_h1, score4_u1_h1, score5_u1_h1, score6_u1_h1, score7_u1_h1])

# 3 days of history
    score1_u1_h2 = Habit_Score(
        id = 8,
        date = "2020-08-03 20:00:00-06",
        score = 70,
        habit_id = 2
    )

    score2_u1_h2 = Habit_Score(
        id = 9,
        date = "2020-08-02 20:00:00-06",
        score = 80.0,
        habit_id = 2
    )

    score3_u1_h2 = Habit_Score(
        id = 10,
        date = "2020-08-01 20:00:00-06",
        score = 90.0,
        habit_id = 2
    )

    db.session.add_all([score1_u1_h2, score2_u1_h2, score3_u1_h2])

# No History for h3
    # score1_u1_h3

# 3 days of history
    score1_u2_h1 = Habit_Score(
        id = 11,
        date = "2020-08-03 20:00:00-06",
        score = 70,
        habit_id = 4
    )

    score2_u2_h1 = Habit_Score(
        id = 12,
        date = "2020-08-02 20:00:00-06",
        score = 95,
        habit_id = 4
    )

    score3_u2_h1 = Habit_Score(
        id = 13,
        date = "2020-08-01 20:00:00-06",
        score = 100,
        habit_id = 4
    )

    db.session.add_all([score1_u2_h1, score2_u2_h1, score3_u2_h1])

# No History for h2
    # score1_u2_h2

# Full week of history
    score1_u2_h3 = Habit_Score(
        id = 14,
        date = "2020-08-02 20:00:00-06",
        score = 100,
        habit_id = 6
    )

    score2_u2_h3 = Habit_Score(
        id = 15,
        date = "2020-08-01 20:00:00-06",
        score = 111,
        habit_id = 6
    )

    score3_u2_h3 = Habit_Score(
        id = 16,
        date = "2020-07-31 20:00:00-06",
        score = 95,
        habit_id = 6
    )

    score4_u2_h3 = Habit_Score(
        id = 17,
        date = "2020-07-30 20:00:00-06",
        score = 105,
        habit_id = 6
    )

    score5_u2_h3 = Habit_Score(
        id = 18,
        date = "2020-07-29 20:00:00-06",
        score = 100,
        habit_id = 6
    )

    score6_u2_h3 = Habit_Score(
        id = 19,
        date = "2020-07-28 20:00:00-06",
        score = 70,
        habit_id = 6
    )

    score7_u2_h3 = Habit_Score(
        id = 20,
        date = "2020-07-27 20:00:00-06",
        score = 55,
        habit_id = 6
    )

    db.session.add_all([score1_u2_h3, score2_u2_h3, score3_u2_h3, score4_u2_h3, score5_u2_h3, score6_u2_h3, score7_u2_h3])
    db.session.commit()



#  GOALS


#  1 week of history
    score1_u1_g1 = Goal_Score(
        id = 1,
        date = "2020-08-03 20:00:00-06",
        score = 50.0,
        goal_id = 1
    )

    score2_u1_g1 = Goal_Score(
        id = 2,
        date = "2020-08-02 20:00:00-06",
        score = 60.0,
        goal_id = 1
    )

    score3_u1_g1 = Goal_Score(
        id = 3,
        date = "2020-08-01 20:00:00-06",
        score = 80.0,
        goal_id = 1
    )

    score4_u1_g1 = Goal_Score(
        id = 4,
        date = "2020-07-31 20:00:00-06",
        score = 65.0,
        goal_id = 1
    )

    score5_u1_g1 = Goal_Score(
        id = 5,
        date = "2020-07-30 20:00:00-06",
        score = 45.0,
        goal_id = 1
    )

    score6_u1_g1 = Goal_Score(
        id = 6,
        date = "2020-07-29 20:00:00-06",
        score = 0.0,
        goal_id = 1
    )

    score7_u1_g1 = Goal_Score(
        id = 7,
        date = "2020-07-28 20:00:00-06",
        score = 90.0,
        goal_id = 1
    )

    db.session.add_all([score1_u1_g1, score2_u1_g1, score3_u1_g1, score4_u1_g1, score5_u1_g1, score6_u1_g1, score7_u1_g1])

# 3 days of history
    score1_u1_g2 = Goal_Score(
        id = 8,
        date = "2020-08-03 20:00:00-06",
        score = 40,
        goal_id = 2
    )

    score2_u1_g2 = Goal_Score(
        id = 9,
        date = "2020-08-02 20:00:00-06",
        score = 70.0,
        goal_id = 2
    )

    score3_u1_g2 = Goal_Score(
        id = 10,
        date = "2020-08-01 20:00:00-06",
        score = 90.0,
        goal_id = 2
    )

    db.session.add_all([score1_u1_g2, score2_u1_g2, score3_u1_g2])

# No History for g3
    # score1_u1_g3

# 3 days of history
    score1_u2_g1 = Goal_Score(
        id = 11,
        date = "2020-08-03 20:00:00-06",
        score = 70,
        goal_id = 4
    )

    score2_u2_g1 = Goal_Score(
        id = 12,
        date = "2020-08-02 20:00:00-06",
        score = 95,
        goal_id = 4
    )

    score3_u2_g1 = Goal_Score(
        id = 13,
        date = "2020-08-01 20:00:00-06",
        score = 45,
        goal_id = 4
    )

    db.session.add_all([score1_u2_g1, score2_u2_h1, score3_u2_g1])

# No History for g2
    # score1_u2_g2

# Full week of history
    score1_u2_g3 = Goal_Score(
        id = 14,
        date = "2020-08-02 20:00:00-06",
        score = 55,
        goal_id = 6
    )

    score2_u2_g3 = Goal_Score(
        id = 15,
        date = "2020-08-01 20:00:00-06",
        score = 75,
        goal_id = 6
    )

    score3_u2_g3 = Goal_Score(
        id = 16,
        date = "2020-07-31 20:00:00-06",
        score = 95,
        goal_id = 6
    )

    score4_u2_g3 = Goal_Score(
        id = 17,
        date = "2020-07-30 20:00:00-06",
        score = 105,
        goal_id = 6
    )

    score5_u2_g3 = Goal_Score(
        id = 18,
        date = "2020-07-29 20:00:00-06",
        score = 100,
        goal_id = 6
    )

    score6_u2_g3 = Goal_Score(
        id = 19,
        date = "2020-07-28 20:00:00-06",
        score = 35,
        goal_id = 6
    )

    score7_u2_g3 = Goal_Score(
        id = 20,
        date = "2020-07-27 20:00:00-06",
        score = 55,
        goal_id = 6
    )

    db.session.add_all([score1_u2_g3, score2_u2_g3, score3_u2_g3, score4_u2_g3, score5_u2_g3, score6_u2_g3, score7_u2_g3])
    db.session.commit()