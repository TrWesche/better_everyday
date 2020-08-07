from flask import Blueprint, render_template, redirect, flash, request, session, g, url_for
from flask import current_app as app
from sqlalchemy import exc

# Import Models
from .models.model_persona import Persona
from .models.model_user_persona import User_Persona
from .models.model_habit import Habit
from .models.model_goal import Goal
from .models.model_user_goal import User_Goal
from .models.model_user_habit import User_Habit

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


# @plan_bp.route("/", methods=["GET"])
# def get_plan_home():
#     user_personas = None
#     user_habits = None
#     user_goals = None

#     if g.user:
#         user_personas = User_Persona.query\
#             .join(Persona, User_Persona.persona_id == Persona.id)\
#             .add_columns(User_Persona.user_id, User_Persona.id, Persona.id, Persona.title, Persona.description)\
#             .filter(User_Persona.user_id == g.user.id).all()

#         user_habits = User_Habit.query\
#             .join(Habit, User_Habit.habit_id == Habit.id)\
#             .add_columns(User_Habit.user_id, User_Habit.id, Habit.id, Habit.title, Habit.description)\
#             .filter(User_Habit.user_id == g.user.id).all()

#         user_goals = User_Goal.query\
#             .join(Goal, User_Goal.goal_id == Goal.id)\
#             .add_columns(User_Goal.user_id, User_Goal.id, Goal.id, Goal.title, Goal.description)\
#             .filter(User_Goal.user_id == g.user.id).all()

#         persona_list = [(persona.id, persona.title) for persona in user_personas]

#         user_persona_form = UserPersonaFrom()

#         user_habit_form = UserHabitForm()
#         user_habit_form.persona.choices = persona_list

#         user_goal_form = UserGoalForm()
#         user_goal_form.persona.choices = persona_list

#         return render_template(
#             "plan_home.html", 
#             user_personas=user_personas, 
#             user_habits=user_habits, 
#             user_goals=user_goals,
#             user_persona_form=user_persona_form,
#             user_habit_form=user_habit_form,
#             user_goal_form=user_goal_form)

#     else:
#         flash("You must be logged in to access that page.", "warning")
#         return redirect(url_for("home_bp.homepage"))

@plan_bp.route("/", methods=["GET"])
def get_plan_home():
    if g.user:

        user_personas = User_Persona.query\
            .join(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(User_Persona.user_id, Persona.title_en, Persona.description_public)\
            .filter(User_Persona.user_id == g.user.id).all()

        user_habits = User_Habit.query\
            .join(Habit, User_Habit.habit_id == Habit.id)\
            .add_columns(User_Habit.user_id, Habit.title_en, Habit.description_public)\
            .join(User_Persona, User_Persona.id == User_Habit.user_persona_id)\
            .add_columns(User_Persona.id.label("persona_id"))\
            .join(Persona, User_Persona.id == Persona.id)\
            .add_columns(Persona.title_en.label("persona_title"))\
            .filter(User_Habit.user_id == g.user.id).all()

        user_goals = User_Goal.query\
            .join(Goal, User_Goal.goal_id == Goal.id)\
            .add_columns(User_Goal.user_id, Goal.title_en, Goal.description_public)\
            .join(User_Persona, User_Persona.id == User_Goal.user_persona_id)\
            .add_columns(User_Persona.id.label("persona_id"))\
            .join(Persona, User_Persona.id == Persona.id)\
            .add_columns(Persona.title_en.label("persona_title"))\
            .filter(User_Goal.user_id == g.user.id).all()

        persona_render_list = []
        if user_personas:
            for persona in user_personas:
                append_obj = {}
                append_obj["user_id"] = persona.user_id
                append_obj["persona_id"] = persona.User_Persona.persona_id
                append_obj["persona_title"] = persona.title_en
                append_obj["description_private"] = persona.User_Persona.description_private
                append_obj["description_public"] = persona.description_public
                append_obj["linked_habits"] = []
                append_obj["linked_goals"] = []

                for habit in user_habits:
                    if habit.User_Habit.user_persona_id == persona.User_Persona.id:
                        append_obj.get("linked_habits").append(habit.title_en)

                for goal in user_goals:
                    if goal.User_Goal.user_persona_id == persona.User_Persona.id:
                        append_obj.get("linked_goals").append(goal.title_en)

                persona_render_list.append(append_obj)

        return render_template("plan_home.html", user_personas = user_personas, user_habits = user_habits, user_goals = user_goals, persona_render_list = persona_render_list)

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
                db.session.rollback()
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
            db.session.rollback()

    return redirect(url_for("plan_bp.get_plan_home"))


@plan_bp.route("/add_user_habit", methods=["POST"])
def add_user_habit():
    form = UserHabitForm(request.form)

    user_personas = User_Persona.query.filter(User_Persona.user_id == g.user.id).all()
    persona_list = [(persona.persona_id, "persona") for persona in user_personas] # This works becuase the validate_on_submit only checks the id (first) value of the tuple
    form.persona.choices = persona_list


    if form.validate_on_submit():
        target_habit = Habit.query.filter(Habit.title == form.title.data.lower()).first()
        target_persona = Persona.query.filter(Persona.id == form.persona.data).first()

        if not target_habit:
            target_habit = Habit(title = form.title.data.lower(), description = form.description.data)
            db.session.add(target_habit)

            try:
                db.session.commit()
            except Exception as e:
                flash("Error: Unable to create new habit", "danger")
                print(e)
                db.session.rollback()
                return redirect(url_for("plan_bp.get_plan_home"))
            
        active = form.active.data
        user_id = g.user.id
        persona_id = target_persona.id
        habit_id = target_habit.id

        # TODO: Add scoring system & schedule selection
        #!!!# Schedules & Scoring Systems will need to be filtered by user_id as well in order to be scalable.  Will require a change in the model.
        #!!!# Future version should only show public scoring_systems/schedules (defaults provided by BE) and the scoring systems created by users.
        scoring_system_id = form.scoring_system_id.data
        schedule_id = form.schedule_id.data

        new_user_habit = User_Habit(
                            active = active, 
                            user_id = user_id, 
                            persona_id = persona_id, 
                            habit_id = habit_id, 
                            scoring_system_id = scoring_system_id, 
                            schedule_id = schedule_id)

        db.session.add(new_user_habit)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new user habit", "danger")
            print(e)
            db.session.rollback()

    return redirect(url_for("plan_bp.get_plan_home"))


# TODO: Implement routes
@plan_bp.route("/add_user_goal", methods=["POST"])
def add_user_goal():
    form = UserGoalForm(request.form)

    #!!!# This sucks there has to be a better way
    user_personas = User_Persona.query.filter(User_Persona.user_id == g.user.id).all()
    persona_list = [(persona.persona_id, "persona") for persona in user_personas] # This works becuase the validate_on_submit only checks the id part of the tuple
    form.persona.choices = persona_list


    if form.validate_on_submit():
        target_goal = Goal.query.filter(Goal.title == form.title.data.lower()).first()
        target_persona = Persona.query.filter(Persona.id == form.persona.data).first()

        if not target_goal:
            target_goal = Goal(title = form.title.data.lower(), description = form.description.data)
            db.session.add(target_goal)

            try:
                db.session.commit()
            except Exception as e:
                flash("Error: Unable to create new goal", "danger")
                print(e)
                db.session.rollback()
                return redirect(url_for("plan_bp.get_plan_home"))
            
        active = form.active.data
        user_id = g.user.id
        persona_id = target_persona.id
        goal_id = target_goal.id

        # TODO: Add scoring system & schedule selection
        #!!!# Schedules & Scoring Systems will need to be filtered by user_id as well in order to be scalable.  Will require a change in the model.
        #!!!# Future version should only show public scoring_systems/schedules (defaults provided by BE) and the scoring systems created by users.
        scoring_system_id = form.scoring_system_id.data
        schedule_id = form.schedule_id.data


        #!!!# The user should also be able to link a goal to a habit in the future
        new_user_goal = User_Goal(
                            active = active, 
                            user_id = user_id, 
                            persona_id = persona_id, 
                            goal_id = goal_id, 
                            scoring_system_id = scoring_system_id, 
                            schedule_id = schedule_id)

        db.session.add(new_user_goal)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new user goal", "danger")
            print(e)
            db.session.rollback()

    return redirect(url_for("plan_bp.get_plan_home"))