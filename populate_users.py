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
        title_en = "User1 Scoring System 1",
        description = "Some Sort of Scoring System 1",
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
