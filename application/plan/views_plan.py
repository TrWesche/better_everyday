from flask import Blueprint, render_template, redirect, flash, request, session, g
from flask import current_app as app
from sqlalchemy import exc
from .models.model_persona import Persona
from .models.model_habit import Habit
from .models.model_goal import Goal
from .models.model_user_persona import User_Persona
from .models.model_user_habit import User_Habit
from .models.model_user_goal import User_Goal
from application import db


# Blueprint Configuration
plan_bp = Blueprint(
    'plan_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


# CURR_USER_KEY = "curr_user"

# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""
#     print("Running Get User Key")
#     print(session.get(CURR_USER_KEY))
#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])
#     else:
#         g.user = None
#     print(g.user)


@plan_bp.route("/", methods=["GET"])
def get_plan_home():
    if g.user:
        user_personas = User_Persona.query\
            .join(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(User_Persona.user_id, User_Persona.id, Persona.id, Persona.title, Persona.description)\
            .filter(User_Persona.user_id == g.user.id).all()

        user_habits = User_Habit.query\
            .join(Habit, User_Habit.habit_id == Habit.id)\
            .add_columns(User_Habit.user_id, User_Habit.id, Habit.id, Habit.title, Habit.description)\
            .filter(User_Habit.user_id == g.user.id).all()

        user_goals = User_Goal.query\
            .join(Goal, User_Goal.goal_id == Goal.id)\
            .add_columns(User_Goal.user_id, User_Goal.id, Goal.id, Goal.title, Goal.description)\
            .filter(User_Goal.user_id == g.user.id).all()

    return render_template("plan_home.html", user_personas=user_personas, user_habits=user_habits, user_goals=user_goals)

# TODO: Implement routes