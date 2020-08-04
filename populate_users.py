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


os.environ['DATABASE_URL'] = "postgres:///better-everyday-test"

from wsgi import app
# from wsgi import app
from application import db

with app.app_context():
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
    )

    u2 = User(
        id = 2,
        first_name="Test",
        last_name="User",
        email="testuser2@test.com",
        username="testuser2",
    )

    db.session.add_all([a1, a2])
    db.session.commit()
    db.session.add_all([u1, u2])
    db.session.commit()


    p1 = Persona(
        id = 1,
        title = "TestPersona1",
        description = "ThisIsATestPersona 1"
    )

    p2 = Persona(
        id = 2,
        title = "TestPersona2",
        description = "ThisIsATestPersona 2"
    )

    h1 = Habit(
        id = 1,
        title = "TestHabit1",
        description = "ThisIsATestHabit 1"
    )

    h2 = Habit(
        id = 2, 
        title = "TestHabit2",
        description = "ThisIsATestHabit 2"
    )

    g1 = Goal(
        id = 1,
        title = "TestGoal1",
        description = "ThisIsATestGoal 1"
    )

    g2 = Goal(
        id = 2,
        title = "TestGoal2",
        description = "ThisIsATestGoal 2"
    )

    db.session.add_all([p1, p2, h1, h2, g1, g2])
    db.session.commit()


    u1_p1 = User_Persona(
        id = 1,
        active = True,
        user_id = 1,
        persona_id = 1
    )

    u1_p2 = User_Persona(
        id = 2,
        active = True,
        user_id = 1,
        persona_id = 2
    )

    u2_p1 = User_Persona(
        id = 3,
        active = True,
        user_id = 2,
        persona_id = 1
    )

    u2_p2 = User_Persona(
        id = 4,
        active = True,
        user_id = 2,
        persona_id = 2
    )

# One Habit per Persona
    u1_h1 = User_Habit(
        id = 1,
        active = True,
        user_id = 1,
        persona_id = 1,
        habit_id = 1
        # scoring_system_id = 1,
        # schedule_id = 1
    )

    u1_h2 = User_Habit(
        id = 2,
        active = True,
        user_id = 1,
        persona_id = 2,
        habit_id = 2
        # scoring_system_id = 1,
        # schedule_id = 1
    )

# One Habit no Persona
    u2_h1 = User_Habit(
        id = 3,
        active = True,
        user_id = 2,
        # persona_id = 2,
        habit_id = 1
        # scoring_system_id = 1,
        # schedule_id = 1
    )

# Mulitple Habits per Persona
    u2_h2 = User_Habit(
        id = 4,
        active = True,
        user_id = 2,
        persona_id = 2,
        habit_id = 1
        # scoring_system_id = 1,
        # schedule_id = 1
    )

    u2_h3 = User_Habit(
        id = 5,
        active = True,
        user_id = 2,
        persona_id = 2,
        habit_id = 2
        # scoring_system_id = 1,
        # schedule_id = 1
    )


# One Goal per Persona
    u1_g1 = User_Goal(
        id = 1,
        active = True,
        user_id = 1,
        persona_id = 1,
        goal_id = 1
        # scoring_system_id = 1,
        # schedule_id = 1
    )

    u1_g2 = User_Goal(
        id = 2,
        active = True,
        user_id = 1,
        persona_id = 2,
        goal_id = 2
        # scoring_system_id = 1,
        # schedule_id = 1
    )

# One Habit no Persona
    u2_g1 = User_Goal(
        id = 3,
        active = True,
        user_id = 2,
        # persona_id = 2,
        goal_id = 1
        # scoring_system_id = 1,
        # schedule_id = 1
    )

# Mulitple Habits per Persona
    u2_g2 = User_Goal(
        id = 4,
        active = True,
        user_id = 2,
        persona_id = 2,
        goal_id = 1
        # scoring_system_id = 1,
        # schedule_id = 1
    )

    u2_g3 = User_Goal(
        id = 5,
        active = True,
        user_id = 2,
        persona_id = 2,
        goal_id = 2
        # scoring_system_id = 1,
        # schedule_id = 1
    )

    db.session.add_all([u1_p1, u1_p2, u2_p1, u2_p2, u1_h1, u1_h2, u2_h1, u2_h2, u2_h3, u1_g1, u1_g2, u2_g1, u2_g2, u2_g3])
    db.session.commit()


    score1 = Scoring_System(
        id = 1,
        title = "Default",
        description = "Default Scoring System",
        public = True
    )

    sched1 = Reminder_Schedule(    
        id = 1,
        title = "Default",
        description = "Default Schedule",
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

    db.session.add_all([score1, sched1])
    db.session.commit()