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

from wsgi import app
from application import db

from application.services.sample_gen.generator_user_goal_scores import generateUserGoalScores
from application.services.sample_gen.generator_user_habit_scores import generateUserHabitScores

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
            first_name="Melissa",
            last_name="McDaniel",
            email="MMcDaniel@betest.com",
            username="testuser1",
            public = True
        )

        u2 = User(
            first_name="Richard",
            last_name="Greenway",
            email="RGreenway@betest.com",
            username="testuser2",
            public = True
        )

        db.session.add_all([a1, a2])
        db.session.commit()
        db.session.add_all([u1, u2])
        db.session.commit()


        p1 = Persona(
            title_en = "Runner",
            description_public = "An athlete with strong cardio ability in running."
        )

        p2 = Persona(
            title_en = "Painter",
            description_public = "An artist who creates physical art with paint and complementary medias."
        )

        p3 = Persona(
            title_en = "Software Engineer",
            description_public = "An engineer specialized in the design, development and maintenance of software."
        )

        p4 = Persona(
            title_en = "Olympian",
            description_public = "An athlete at the top of their physical and mental state representing their nation in global competition."
        )

        p5 = Persona(
            title_en = "Rock Star",
            description_public = "An musician with a notable following who writes and performs music identified as the rock genre."
        )

        # User 1 & User 2
        h1 = Habit(
            title_en = "Stretch",
            description_public = "An activity to increase physical mobility and encourage recovery."
        )

        # User 1
        h2 = Habit(
            title_en = "Run",
            description_public = "The activity of running / propelling yourself by foot."
        )

        # User 1 & User 2
        h3 = Habit(
            title_en = "Healthy Diet",
            description_public = "Follow a diet which encourages physical health."
        )

        # User 1 & User 2
        h4 = Habit(
            title_en = "Sketch",
            description_public = "Catalogue & experiment in artistic design through rough sketching."
        )

        # User 1 & User 2
        h5 = Habit(
            title_en = "Paint",
            description_public = "Create physical art utilizing."
        )

        # User 2
        h6 = Habit(
            title_en = "Code",
            description_public = "Write code to create projects and/or practice new concepts."
        )

         # User 2
        h7 = Habit(
            title_en = "Curl",
            description_public = "Engage in the fine sport of curling."
        )

        # User 1
        h8 = Habit(
            title_en = "Sing",
            description_public = "Seranade audiences, loved ones, or your wall with your lovely voice."
        )

        # User 1
        g1 = Goal(
            title_en = "Run 25kms in a single session",
            description_public = "Half marathon preparation"
        )

        # User 1
        g2 = Goal(
            title_en = "Run 50kms in a single session",
            description_public = "Full marathon preparation."
        )

        # User 1
        g3 = Goal(
            title_en = "Sketch The Thinker from online images",
            description_public = "Practice human biology in sketch."
        )

        # User 2
        g4 = Goal(
            title_en = "Paint an image of a Lily",
            description_public = "Create first full color image of a flower."
        )
        
        # User 2
        g5 = Goal(
            title_en = "Finish Capstone 1 Project",
            description_public = "Complete first full-stack project for programming course."
        )

        # User 2
        g6 = Goal(
            title_en = "Hit the Button 10 times in a row",
            description_public = "Land stone in the center of the scoring area 10 times in a row in practice."
        )
        
        # User 1
        g7 = Goal(
            title_en = "Complete lyrics for first song",
            description_public = "Finish writing lyrics for first song release."
        )
     
        # User 1
        g8 = Goal(
            title_en = "Master the guitar lick for recording",
            description_public = "Practice the guitar line for first song in preparation for recording."
        )

        db.session.add_all([p1, p2, p3, p4, p5, h1, h2, h3, h4, h5, h6, h7, h8, g1, g2, g3, g4, g5, g6, g7, g8])
        db.session.commit()

        score1 = Scoring_System(
            user_id = u1.id,
            title_en = "US Grading System",
            description = "US Grading System",
            public = False
        )

        score2 = Scoring_System(
            user_id = u1.id,
            title_en = "All or Nothing Scoring System 30mins",
            description = "Only credit if time spent is greater than 30mins",
            public = False
        )

        score3 = Scoring_System(
            user_id = u2.id,
            title_en = "Back Loaded Scoring System",
            description = "Progressively higher scores given for more time spent",
            public = False
        )

        score4 = Scoring_System(
            user_id = u2.id,
            title_en = "Motivational Message Scoring System",
            description = "Scores are accopanied by motivational messages.",
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
            score_input = 29,
            score_output = 0,
            name_en = None
        )

        score2_param_3 = Scoring_System_Params(
            scoring_system_id = score2.id,
            score_bp = 2,
            score_input = 30,
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
            score_input = 30,
            score_output = 5,
            name_en = None
        )

        score3_param_4 = Scoring_System_Params(
            scoring_system_id = score3.id,
            score_bp = 3,
            score_input = 45,
            score_output = 10,
            name_en = None
        )

        score3_param_5 = Scoring_System_Params(
            scoring_system_id = score3.id,
            score_bp = 4,
            score_input = 55,
            score_output = 15,
            name_en = None
        )

        score3_param_6 = Scoring_System_Params(
            scoring_system_id = score3.id,
            score_bp = 5,
            score_input = 60,
            score_output = 20,
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
            name_en = "A true champion!"
        )

        db.session.add_all([score1_param_1, score1_param_2, score1_param_3, score1_param_4, score1_param_5, score1_param_6, score2_param_1, 
                            score2_param_2, score2_param_3, score3_param_1, score3_param_2, score3_param_3, score3_param_4, score3_param_5,
                            score3_param_6, score4_param_1, score4_param_2, score4_param_3, score4_param_4])
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

        u1_p5 = User_Persona(
            active = True,
            user_id = u1.id,
            persona_id = p5.id,
            description_private = "I'll be the best rockstar in the world, like Queen meets Slipknot."
        )

        u2_p2 = User_Persona(
            active = True,
            user_id = u2.id,
            persona_id = p2.id,
            description_private = "A new hobby to relax to, who doesn't like happy clouds?"
        )

        u2_p3 = User_Persona(
            active = True,
            user_id = u2.id,
            persona_id = p3.id,
            description_private = "I've always wanted to create the next Facebook."
        )

        u2_p4 = User_Persona(
            active = True,
            user_id = u2.id,
            persona_id = p4.id,
            description_private = None
        )

        db.session.add_all([u1_p1, u1_p2, u1_p5, u2_p2, u2_p3, u2_p4])
        db.session.commit()

    # User 1 Goals
        # Goal run 25kms
        u1_g1 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            goal_id = g1.id,
            description_private = None
        )

        # Goal run 50kms
        u1_g2 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            goal_id = g2.id,
            description_private = None
        )

        # Sketch the Thinker
        u1_g3 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p2.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            goal_id = g3.id,
            description_private = None
        )

        # Write song lyrics
        u1_g4 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p5.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            goal_id = g7.id,
            description_private = "Gritty & politically charged or a party song?"
        )

        # Master Guitar
        u1_g5 = User_Goal(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p5.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            goal_id = g8.id,
            description_private = "I will seranade the gods with my guitar mastery"
        )

        # User 2 Goals
        # Paint a Lily
        u2_g1 = User_Goal(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p2.id,
            scoring_system_id = score3.id,
            schedule_id = sched1.id,
            goal_id = g4.id,
            description_private = None
        )

        # Finish Capstone
        u2_g2 = User_Goal(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p3.id,
            scoring_system_id = score4.id,
            schedule_id = sched2.id,
            goal_id = g5.id,
            description_private = "This website will change the world!  Well maybe not, but its a start."
        )

        # Curling bullseye
        u2_g3 = User_Goal(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p4.id,
            scoring_system_id = score3.id,
            schedule_id = sched2.id,
            goal_id = g6.id,
            description_private = None
        )


        db.session.add_all([u1_g1, u1_g2, u1_g3, u1_g4, u1_g5, u2_g1, u2_g2, u2_g3])
        db.session.commit()

        # user 1 Habits
        # Stretch
        u1_h1 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            habit_id = h1.id,
            linked_goal_id = None,
            description_private = "I've had alot of shin splint problems in the past"
        )

        # Run
        u1_h2 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            habit_id = h2.id,
            linked_goal_id = None,
            description_private = None
        )

        # Healthy Diet
        u1_h3 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p1.id,
            scoring_system_id = score1.id,
            schedule_id = sched1.id,
            habit_id = h3.id,
            linked_goal_id = None,
            description_private = "No more Twinkies!"
        )

        # Sketch
        u1_h4 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p2.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            habit_id = h4.id,
            linked_goal_id = None,
            description_private = None
        )

        # Paint
        u1_h5 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p2.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            habit_id = h5.id,
            linked_goal_id = None,
            description_private = None
        )

        # Sing
        u1_h6 = User_Habit(
            active = True,
            user_id = u1.id,
            user_persona_id = u1_p5.id,
            scoring_system_id = score2.id,
            schedule_id = sched1.id,
            habit_id = h8.id,
            linked_goal_id = None,
            description_private = "Screaming needs some work"
        )

        # User 2 Habits
        # Stretch
        u2_h1 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p4.id,
            scoring_system_id = score3.id,
            schedule_id = sched1.id,
            habit_id = h1.id,
            linked_goal_id = None,
            description_private = "Need to make sure my hips are loose for letting that stone go"
        )

        # Healthy Diet
        u2_h2 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p4.id,
            scoring_system_id = score3.id,
            schedule_id = sched1.id,
            habit_id = h3.id,
            linked_goal_id = None,
            description_private = None
        )

        # Sketch
        u2_h3 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p2.id,
            scoring_system_id = score4.id,
            schedule_id = sched1.id,
            habit_id = h4.id,
            linked_goal_id = None,
            description_private = None
        )

        # Paint
        u2_h4 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p2.id,
            scoring_system_id = score4.id,
            schedule_id = sched1.id,
            habit_id = h5.id,
            linked_goal_id = None,
            description_private = None
        )

        # Code
        u2_h5 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p3.id,
            scoring_system_id = score3.id,
            schedule_id = sched1.id,
            habit_id = h6.id,
            linked_goal_id = None,
            description_private = None
        )

        # Code
        u2_h6 = User_Habit(
            active = True,
            user_id = u2.id,
            user_persona_id = u2_p4.id,
            scoring_system_id = score3.id,
            schedule_id = sched1.id,
            habit_id = h7.id,
            linked_goal_id = None,
            description_private = None
        )

        db.session.add_all([u1_h1, u1_h2, u1_h3, u1_h4, u1_h5, u1_h6, u2_h1, u2_h2, u2_h3, u2_h4, u2_h5, u2_h6])
        db.session.commit()


        generateUserGoalScores(30, u1_g1.id, 0, 100)
        generateUserGoalScores(20, u1_g2.id, 0, 100)
        generateUserGoalScores(30, u1_g3.id, 0, 100)
        generateUserGoalScores(25, u1_g4.id, 0, 100)
        generateUserGoalScores(15, u1_g5.id, 0, 100)
        generateUserGoalScores(25, u2_g1.id, 0, 100)
        generateUserGoalScores(15, u2_g2.id, 0, 100)
        generateUserGoalScores(30, u2_g3.id, 0, 100)

        generateUserHabitScores(30, u1_h1.id, 0, 100)
        generateUserHabitScores(30, u1_h2.id, 0, 100)
        generateUserHabitScores(20, u1_h3.id, 0, 100)
        generateUserHabitScores(30, u1_h4.id, 0, 100)
        generateUserHabitScores(25, u1_h5.id, 0, 100)
        generateUserHabitScores(30, u1_h6.id, 0, 100)
        generateUserHabitScores(30, u2_h1.id, 0, 100)
        generateUserHabitScores(30, u2_h2.id, 0, 100)
        generateUserHabitScores(15, u2_h3.id, 0, 100)
        generateUserHabitScores(10, u2_h4.id, 0, 100)
        generateUserHabitScores(20, u2_h5.id, 0, 100)
        generateUserHabitScores(30, u2_h6.id, 0, 100)
