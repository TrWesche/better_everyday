from flask import Blueprint, render_template, redirect, flash, request, session, g, url_for
from flask import current_app as app
from sqlalchemy import exc

# Import Models
from .models.model_persona import Persona
from .models.model_habit import Habit
from .models.model_goal import Goal
from .models.model_user_persona import User_Persona
from .models.model_user_habit import User_Habit
from .models.model_user_goal import User_Goal

# Import Forms
from .forms.form_user_persona import UserPersonaFrom
from .forms.form_user_habit import UserHabitForm
from .forms.form_user_goal import UserGoalForm

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
    user_personas = None
    user_habits = None
    user_goals = None

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

        persona_list = [(persona.id, persona.title) for persona in user_personas]
        print(persona_list)

        user_persona_form = UserPersonaFrom()

        user_habit_form = UserHabitForm()
        user_habit_form.persona.choices = persona_list

        user_goal_form = UserGoalForm()
        user_goal_form.persona.choices = persona_list

        return render_template(
            "plan_home.html", 
            user_personas=user_personas, 
            user_habits=user_habits, 
            user_goals=user_goals,
            user_persona_form=user_persona_form,
            user_habit_form=user_habit_form,
            user_goal_form=user_goal_form)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

# TODO: Convert to AJAX
@plan_bp.route("/add_user_persona", methods=["POST"])
def add_user_persona():
    form = UserPersonaFrom(request.form)

    if form.validate_on_submit():
        target_persona = Persona.query.filter(Persona.title == form.title.data.lower()).first()

        if not target_persona:
            target_persona = Persona(title = form.title.data.lower(), description = form.description.data)
            db.session.add(target_persona)

            try:
                db.session.commit()
            except Exception as e:
                flash("Error: Unable to create new persona", "danger")
                print(e)
                return redirect(url_for("plan_bp.get_plan_home"))

        active = form.active.data
        user_id = g.user.id
        persona_id = target_persona.id

        new_user_persona = User_Persona(active = active, user_id = user_id, persona_id = persona_id)

        db.session.add(new_user_persona)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new persona", "danger")
            print(e)

    return redirect(url_for("plan_bp.get_plan_home"))

# TODO: Implement routes
@plan_bp.route("/add_user_habit", methods=["POST"])
def add_user_habit():
    return redirect(url_for("plan_bp.get_plan_home"))

# TODO: Implement routes
@plan_bp.route("/add_user_goal", methods=["POST"])
def add_user_goal():
    return redirect(url_for("plan_bp.get_plan_home"))