# import os

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

# os.environ['DATABASE_URL'] = "postgres:///better-everyday-test-v2"

from wsgi import app
from application import db

def seed_demo():

    with app.app_context():
        # Password = password
        db.drop_all()
        db.create_all()

        a1 = Authentication(
            username="testuser1",
            password="$2b$12$gyjYvEBqcebZBKiX3C8OGO5cNiXmNVFdzVbcNdxE/eCruG4I5lEOG"
        )

        a2 = Authentication(
            username="testuser2",
            password="$2b$12$gyjYvEBqcebZBKiX3C8OGO5cNiXmNVFdzVbcNdxE/eCruG4I5lEOG"
        )

        u1 = User(
            first_name="Test",
            last_name="User",
            email="testuser1@test.com",
            username="testuser1",
            public = True
        )

        u2 = User(
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
            title_en = "testpersona1",
            description_public = "ThisIsAPublicDescription Persona 1"
        )

        p2 = Persona(
            title_en = "testpersona2",
            description_public = "ThisIsAPublicDescription Persona 2"
        )

        p3 = Persona(
            title_en = "testpersona3",
            description_public = "ThisIsAPublicDescription Persona 3"
        )

        h1 = Habit(
            title_en = "testhabit1",
            description_public = "ThisIsAPublicDescription Habit 1"
        )

        h2 = Habit(
            title_en = "testhabit2",
            description_public = "ThisIsAPublicDescription Habit 2"
        )

        h3 = Habit(
            title_en = "testhabit3",
            description_public = "ThisIsAPublicDescription Habit 3"
        )

        g1 = Goal(
            title_en = "testgoal1",
            description_public = "ThisIsAPublicDescription Goal 1"
        )

        g2 = Goal(
            title_en = "testgoal2",
            description_public = "ThisIsAPublicDescription Goal 2"
        )

        g3 = Goal(
            title_en = "testgoal3",
            description_public = "ThisIsAPublicDescription Goal 3"
        )


        db.session.add_all([p1, p2, p3, h1, h2, h3, g1, g2, g3])
        db.session.commit()

        score1 = Scoring_System(
            user_id = u1.id,
            title_en = "User1 US Grades System 1",
            description = "US Grading System 1",
            public = False
        )

        score2 = Scoring_System(
            user_id = u1.id,
            title_en = "User1 Scoring System 2",
            description = "Some Sort of Scoring System 1",
            public = False
        )

        score3 = Scoring_System(
            user_id = u2.id,
            title_en = "User2 Scoring System 3",
            description = "Some Sort of Scoring System 3",
            public = False
        )

        score4 = Scoring_System(
            user_id = u2.id,
            title_en = "User1 Scoring System 4",
            description = "Some Sort of Scoring System 4",
            public = False
        )

    


        sched1 = Reminder_Schedule(    
            user_id = u1.id,
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
            user_id = u1.id,
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
            scoring_system_id = score1.id,
            score_bp = 0,
            score_input = 0,
            score_output = 0,
            name_en = "F"
        )

        score1_param_2 = Scoring_System_Params(
            scoring_system_id = score1.id,
            score_bp = 1,
            score_input = 59,
            score_output = 0,
            name_en = "F"
        )

        score1_param_3 = Scoring_System_Params(
            scoring_system_id = score1.id,
            score_bp = 2,
            score_input = 69,
            score_output = 1,
            name_en = "D"
        )

        score1_param_4 = Scoring_System_Params(
            scoring_system_id = score1.id,
            score_bp = 3,
            score_input = 79,
            score_output = 2,
            name_en = "C"
        )

        score1_param_5 = Scoring_System_Params(
            scoring_system_id = score1.id,
            score_bp = 4,
            score_input = 89,
            score_output = 3,
            name_en = "B"
        )

        score1_param_6 = Scoring_System_Params(
            scoring_system_id = score1.id,
            score_bp = 5,
            score_input = 100,
            score_output = 4,
            name_en = "A"
        )

        score2_param_1 = Scoring_System_Params(
            scoring_system_id = score2.id,
            score_bp = 0,
            score_input = 0,
            score_output = 0,
            name_en = None
        )

        score2_param_2 = Scoring_System_Params(
            scoring_system_id = score2.id,
            score_bp = 1,
            score_input = 50,
            score_output = 2,
            name_en = None
        )

        score2_param_3 = Scoring_System_Params(
            scoring_system_id = score2.id,
            score_bp = 2,
            score_input = 100,
            score_output = 5,
            name_en = None
        )

        score3_param_1 = Scoring_System_Params(
            scoring_system_id = score3.id,
            score_bp = 0,
            score_input = 0,
            score_output = 0,
            name_en = None
        )

        score3_param_2 = Scoring_System_Params(
            scoring_system_id = score3.id,
            score_bp = 1,
            score_input = 10,
            score_output = 1,
            name_en = None
        )

        score3_param_3 = Scoring_System_Params(
            scoring_system_id = score3.id,
            score_bp = 2,
            score_input = 60,
            score_output = 5,
            name_en = None
        )

        score3_param_4 = Scoring_System_Params(
            scoring_system_id = score3.id,
            score_bp = 3,
            score_input = 90,
            score_output = 10,
            name_en = None
        )

        score4_param_1 = Scoring_System_Params(
            scoring_system_id = score4.id,
            score_bp = 0,
            score_input = 0,
            score_output = 0,
            name_en = "You can do better then that!"
        )

        score4_param_2 = Scoring_System_Params(
            scoring_system_id = score4.id,
            score_bp = 1,
            score_input = 30,
            score_output = 50,
            name_en = "Just a little more!"
        )

        score4_param_3 = Scoring_System_Params(
            scoring_system_id = score4.id,
            score_bp = 2,
            score_input = 60,
            score_output = 100,
            name_en = "Target Achieved!"
        )

        score4_param_4 = Scoring_System_Params(
            scoring_system_id = score4.id,
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
            active = True,
            user_id = u1.id,
            persona_id = p1.id,
            description_private = None
        )

        u1_p2 = User_Persona(
            active = True,
            user_id = u1.id,
            persona_id = p2.id,
            description_private = None
        )

        u1_p3 = User_Persona(
            active = True,
            user_id = u1.id,
            persona_id = p3.id,
            description_private = "This is a private description Persona 3"
        )

        u2_p1 = User_Persona(
            active = True,
            user_id = u2.id,
            persona_id = p1.id,
            description_private = "This is a private description Persona 1"
        )

        u2_p2 = User_Persona(
            active = True,
            user_id = u2.id,
            persona_id = p2.id,
            description_private = "This is a private description Persona 2"
        )

        u2_p3 = User_Persona(
            active = True,
            user_id = u2.id,
            persona_id = p3.id,
            description_private = None
        )

        db.session.add_all([u1_p1, u1_p2, u1_p3, u2_p1, u2_p2, u2_p3])
        db.session.commit()

    # One Goal per Persona
        u1_g1 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            goal_id = g1.id,
            description_private = None
        )

        u1_g2 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p2.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            goal_id = g2.id,
            description_private = None
        )

        u1_g3 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            goal_id = g3.id,
            description_private = "This is a private description Goal 3"
        )

    # One Goal no Persona
        u2_g1 = User_Goal(
            active = True,
            user_id = u2.id,
            user_persona_id = None,
            scoring_system_id = score3.id,
            schedule_id = sched1.id,
            goal_id = g1.id,
            description_private = "This is a private description Goal 1"
        )

    # Mulitple Goals per Persona
        u2_g2 = User_Goal(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p2.id,
            scoring_system_id = score4.id,
            schedule_id = sched2.id,
            goal_id = g2.id,
            description_private = "This is a private description Goal 2"
        )

        u2_g3 = User_Goal(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p3.id,
            scoring_system_id = score3.id,
            schedule_id = sched2.id,
            goal_id = g3.id,
            description_private = None
        )

        db.session.add_all([u1_g1, u1_g2, u1_g3, u2_g1, u2_g2, u2_g3])
        db.session.commit()



    # One Habit per Persona
        u1_h1 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            habit_id = h1.id,
            linked_goal_id = None,
            description_private = "This is a private description Habit 1"
        )

        u1_h2 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p2.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            habit_id = h2.id,
            linked_goal_id = None,
            description_private = "This is a private description Habit 2"
        )

        u1_h3 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            habit_id = h3.id,
            linked_goal_id = u1_g2.id,
            description_private = None
        )

    # One Habit no Persona
        u2_h1 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = None,
            scoring_system_id = score3.id,
            schedule_id = sched2.id,
            habit_id = h1.id,
            linked_goal_id = None,
            description_private = None
        )

    # Mulitple Habits per Persona
        u2_h2 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p2.id,
            scoring_system_id = score4.id,
            schedule_id = sched2.id,
            habit_id = h2.id,
            linked_goal_id = None,
            description_private = None
        )

        u2_h3 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p2.id,
            scoring_system_id = score3.id,
            schedule_id = sched2.id,
            habit_id = h3.id,
            linked_goal_id = None,
            description_private = "This is a private description Habit 3"
        )

        db.session.add_all([u1_h1, u1_h2, u1_h3, u2_h1, u2_h2, u2_h3])
        db.session.commit()


    #  1 week of history
        score1_u1_h1 = Habit_Score(
            date = datetime.today(),
            score = 50.0,
            habit_id = u1_h1.id
        )

        score2_u1_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=1),
            score = 60.0,
            habit_id = u1_h1.id
        )

        score3_u1_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=2),
            score = 80.0,
            habit_id = u1_h1.id
        )

        score4_u1_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=3),
            score = 65.0,
            habit_id = u1_h1.id
        )

        score5_u1_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=4),
            score = 45.0,
            habit_id = u1_h1.id
        )

        score6_u1_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=5),
            score = 0.0,
            habit_id = u1_h1.id
        )

        score7_u1_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=6),
            score = 90.0,
            habit_id = u1_h1.id
        )

        db.session.add_all([score1_u1_h1, score2_u1_h1, score3_u1_h1, score4_u1_h1, score5_u1_h1, score6_u1_h1, score7_u1_h1])

    # 3 days of history
        score1_u1_h2 = Habit_Score(
            date = datetime.today(),
            score = 70,
            habit_id = u1_h2.id
        )

        score2_u1_h2 = Habit_Score(
            date = datetime.today() - timedelta(days=1),
            score = 80.0,
            habit_id = u1_h2.id
        )

        score3_u1_h2 = Habit_Score(
            date = datetime.today() - timedelta(days=2),
            score = 90.0,
            habit_id = u1_h2.id
        )

        db.session.add_all([score1_u1_h2, score2_u1_h2, score3_u1_h2])

    # No History for h3
        # score1_u1_h3

    # 3 days of history
        score1_u2_h1 = Habit_Score(
            date = datetime.today(),
            score = 70,
            habit_id = u2_h1.id
        )

        score2_u2_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=1),
            score = 95,
            habit_id = u2_h1.id
        )

        score3_u2_h1 = Habit_Score(
            date = datetime.today() - timedelta(days=2),
            score = 100,
            habit_id = u2_h1.id
        )

        db.session.add_all([score1_u2_h1, score2_u2_h1, score3_u2_h1])

    # No History for h2
        # score1_u2_h2

    # Full week of history
        score1_u2_h3 = Habit_Score(
            date = datetime.today(),
            score = 100,
            habit_id = u2_h3.id
        )

        score2_u2_h3 = Habit_Score(
            date = datetime.today() - timedelta(days=1),
            score = 111,
            habit_id = u2_h3.id
        )

        score3_u2_h3 = Habit_Score(
            date = datetime.today() - timedelta(days=2),
            score = 95,
            habit_id = u2_h3.id
        )

        score4_u2_h3 = Habit_Score(
            date = datetime.today() - timedelta(days=3),
            score = 105,
            habit_id = u2_h3.id
        )

        score5_u2_h3 = Habit_Score(
            date = datetime.today() - timedelta(days=4),
            score = 100,
            habit_id = u2_h3.id
        )

        score6_u2_h3 = Habit_Score(
            date = datetime.today() - timedelta(days=5),
            score = 70,
            habit_id = u2_h3.id
        )

        score7_u2_h3 = Habit_Score(
            date = datetime.today() - timedelta(days=6),
            score = 55,
            habit_id = u2_h3.id
        )

        db.session.add_all([score1_u2_h3, score2_u2_h3, score3_u2_h3, score4_u2_h3, score5_u2_h3, score6_u2_h3, score7_u2_h3])
        db.session.commit()


    # ----------------------
    #  GOALS
    # ----------------------

    #  1 week of history
        score1_u1_g1 = Goal_Score(
            date = datetime.today(),
            score = 50.0,
            goal_id = u1_g1.id
        )

        score2_u1_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=1),
            score = 60.0,
            goal_id = u1_g1.id
        )

        score3_u1_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=2),
            score = 80.0,
            goal_id = u1_g1.id
        )

        score4_u1_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=3),
            score = 65.0,
            goal_id = u1_g1.id
        )

        score5_u1_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=4),
            score = 45.0,
            goal_id = u1_g1.id
        )

        score6_u1_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=5),
            score = 0.0,
            goal_id = u1_g1.id
        )

        score7_u1_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=6),
            score = 90.0,
            goal_id = u1_g1.id
        )

        db.session.add_all([score1_u1_g1, score2_u1_g1, score3_u1_g1, score4_u1_g1, score5_u1_g1, score6_u1_g1, score7_u1_g1])

    # 3 days of history
        score1_u1_g2 = Goal_Score(
            date = datetime.today(),
            score = 70,
            goal_id = u1_g2.id
        )

        score2_u1_g2 = Goal_Score(
            date = datetime.today() - timedelta(days=1),
            score = 80.0,
            goal_id = u1_g2.id
        )

        score3_u1_g2 = Goal_Score(
            date = datetime.today() - timedelta(days=2),
            score = 90.0,
            goal_id = u1_g2.id
        )

        db.session.add_all([score1_u1_g2, score2_u1_g2, score3_u1_g2])

    # No History for g3
        # score1_u1_g3

    # 3 days of history
        score1_u2_g1 = Goal_Score(
            date = datetime.today(),
            score = 70,
            goal_id = u2_g1.id
        )

        score2_u2_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=1),
            score = 95,
            goal_id = u2_g1.id
        )

        score3_u2_g1 = Goal_Score(
            date = datetime.today() - timedelta(days=2),
            score = 100,
            goal_id = u2_g1.id
        )

        db.session.add_all([score1_u2_g1, score2_u2_h1, score3_u2_g1])

    # No History for g2
        # score1_u2_g2

    # Full week of history
        score1_u2_g3 = Goal_Score(
            date = datetime.today(),
            score = 100,
            goal_id = u2_g3.id
        )

        score2_u2_g3 = Goal_Score(
            date = datetime.today() - timedelta(days=1),
            score = 111,
            goal_id = u2_g3.id
        )

        score3_u2_g3 = Goal_Score(
            date = datetime.today() - timedelta(days=2),
            score = 95,
            goal_id = u2_g3.id
        )

        score4_u2_g3 = Goal_Score(
            date = datetime.today() - timedelta(days=3),
            score = 105,
            goal_id = u2_g3.id
        )

        score5_u2_g3 = Goal_Score(
            date = datetime.today() - timedelta(days=4),
            score = 100,
            goal_id = u2_g3.id
        )

        score6_u2_g3 = Goal_Score(
            date = datetime.today() - timedelta(days=5),
            score = 70,
            goal_id = u2_g3.id
        )

        score7_u2_g3 = Goal_Score(
            date = datetime.today() - timedelta(days=6),
            score = 55,
            goal_id = u2_g3.id
        )

        db.session.add_all([score1_u2_g3, score2_u2_g3, score3_u2_g3, score4_u2_g3, score5_u2_g3, score6_u2_g3, score7_u2_g3])
        db.session.commit()