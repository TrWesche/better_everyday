from flask import Blueprint, render_template, redirect, flash, request, session, g, url_for
from flask import current_app as app
from sqlalchemy import exc, or_, and_
import functools

# Import Models
from .models.model_persona import Persona
from .models.model_user_persona import User_Persona
from .models.model_habit import Habit
from .models.model_goal import Goal
from .models.model_user_goal import User_Goal
from .models.model_user_habit import User_Habit

from ..tracking.models.model_scoring_system import Scoring_System
from ..tracking.models.model_scoring_system_params import Scoring_System_Params
from ..tracking.models.model_reminder_schedule import Reminder_Schedule

# Import Forms
from .forms.form_user_persona import UserPersonaForm
from .forms.form_user_habit import UserHabitForm
from .forms.form_user_goal import UserGoalForm

from application import db



# Blueprint Configuration
plan_bp = Blueprint(
    'plan_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

msg_not_logged_in = "Please login to continue."
msg_not_authorized = "You are not authorized to view that resource."
msg_not_found = "We were unable to retrieve the specified entry."

def login_required(func):
    """Make sure user is logged in before proceeding"""
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if not g.user:
            flash(msg_not_logged_in, "warning")
            return redirect(url_for("home_bp.homepage"))
        return func(*args, **kwargs)
    return wrapper_login_required

def query_all_user_personas(user_id):
    query_result = User_Persona.query\
        .join(Persona, User_Persona.persona_id == Persona.id)\
        .add_columns(User_Persona.user_id, Persona.title_en, Persona.description_public)\
        .filter(User_Persona.user_id == user_id).all()
    return query_result

def query_one_user_persona(user_id, persona_id):
    query_result = User_Persona.query\
        .filter(and_(User_Persona.user_id == user_id, User_Persona.id == persona_id)).first()
    return query_result

def query_one_user_persona_dict_join(user_id, persona_id):
    query_result = User_Persona.query\
        .join(Persona, User_Persona.persona_id == Persona.id)\
        .add_columns(User_Persona.user_id, Persona.title_en, Persona.description_public)\
        .filter(and_(User_Persona.user_id == user_id, User_Persona.id == persona_id)).first()
    return query_result

def query_all_user_habits(user_id):
    query_result = User_Habit.query\
        .join(Habit, User_Habit.habit_id == Habit.id)\
        .add_columns(User_Habit.user_id, Habit.title_en, Habit.description_public)\
        .outerjoin(User_Persona, User_Persona.id == User_Habit.user_persona_id)\
        .add_columns(User_Persona.id.label("persona_id"))\
        .outerjoin(Persona, User_Persona.persona_id == Persona.id)\
        .add_columns(Persona.title_en.label("persona_title"))\
        .filter(User_Habit.user_id == user_id).all()
    return query_result

def query_one_user_habit_dict_join(user_id, habit_id):
    query_result = User_Habit.query\
        .join(Habit, User_Habit.habit_id == Habit.id)\
        .add_columns(User_Habit.user_id, Habit.title_en, Habit.description_public)\
        .filter(and_(User_Habit.user_id == user_id, User_Habit.id == habit_id)).first()
    return query_result

def query_one_user_habit(user_id, habit_id):
    query_result =User_Habit.query\
        .filter(and_(User_Habit.user_id == user_id, User_Habit.id == habit_id)).first()
    return query_result

def query_all_user_goals(user_id):
    query_result = User_Goal.query\
        .join(Goal, User_Goal.goal_id == Goal.id)\
        .add_columns(User_Goal.user_id, Goal.title_en, Goal.description_public)\
        .outerjoin(User_Persona, User_Persona.id == User_Goal.user_persona_id)\
        .add_columns(User_Persona.id.label("persona_id"))\
        .outerjoin(Persona, User_Persona.persona_id == Persona.id)\
        .add_columns(Persona.title_en.label("persona_title"))\
        .filter(User_Goal.user_id == user_id).all()
    return query_result

def query_one_user_goal_dict_join(user_id, goal_id):
    query_result = User_Goal.query\
        .join(Goal, User_Goal.goal_id == Goal.id)\
        .add_columns(User_Goal.user_id, Goal.title_en, Goal.description_public)\
        .filter(and_(User_Goal.user_id == user_id, User_Goal.id == goal_id)).first()
    return query_result

def query_one_user_goal(user_id, goal_id):
    query_result = User_Goal.query\
        .filter(and_(User_Goal.user_id == user_id, User_Goal.id == goal_id)).first()
    return query_result

@plan_bp.route("/", methods=["GET"])
def get_plan_home():
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # Get User Personas, Habits, and Goals
    user_personas = query_all_user_personas(g.user.id)
    user_habits = query_all_user_habits(g.user.id)
    user_goals = query_all_user_goals(g.user.id)

    persona_render_list = []
    if user_personas:
        for persona in user_personas:
            append_obj = {}
            append_obj["id"] = persona.User_Persona.id
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


##########################
# CrUD - Persona Routes
##########################

# Create Persona
@plan_bp.route("/persona/new", methods=["GET"])
@login_required
def get_new_persona():
    user_persona_form = UserPersonaForm()
    return render_template("plan_new_persona.html",
            user_persona_form=user_persona_form)

@plan_bp.route("/persona/new", methods=["POST"])
@login_required
def add_user_persona():
    # Re-render page if unable to validate form data
    form = UserPersonaForm(request.form)
    if not form.validate_on_submit():
        return render_template("plan_new_persona.html", user_persona_form=form)

    # Check to see if Persona exists and create if it does not
    target_persona = Persona.query.filter(Persona.title_en == form.title.data.lower()).first()
    if not target_persona:
        target_persona = Persona(title_en = form.title.data.lower())
        db.session.add(target_persona)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new persona", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_new_persona"))

    # Create new User Persona entry utilizing the id data from the queried/created persona
    active = form.active.data
    user_id = g.user.id
    persona_id = target_persona.id

    new_user_persona = User_Persona(active = active, user_id = user_id, persona_id = persona_id, description_private = form.description.data)
    db.session.add(new_user_persona)
    try:
        db.session.commit()
    except Exception as e:
        flash("Error: Unable to create new persona", "danger")
        print(e)
        db.session.rollback()

    return redirect(url_for("plan_bp.get_plan_home"))

# Update Persona
@plan_bp.route("/persona/<int:persona_id>/edit", methods=["GET"])
@login_required
def get_edit_persona(persona_id):
     # Check that User Persona and User ID combo exists, if not unauthorized access
    target_user_persona = query_one_user_persona_dict_join(g.user.id, persona_id)
    if not target_user_persona:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    # Create user form and render page
    user_persona_form = UserPersonaForm(
        title = target_user_persona.title_en,
        description = target_user_persona.User_Persona.description_private,
        active = target_user_persona.User_Persona.active
    )
    return render_template("plan_edit_persona.html",
            user_persona_form=user_persona_form, persona_id=persona_id)

@plan_bp.route("/persona/<int:persona_id>/edit", methods=["POST"])
@login_required
def update_persona(persona_id):
    # Re-render page if unable to validate form data
    form = UserPersonaForm(request.form)
    if not form.validate_on_submit(): 
        return render_template("plan_edit_persona.html", user_persona_form=form)

     # Check that User Persona and User ID combo exists, if not unauthorized access
    target_user_persona = query_one_user_persona(g.user.id, persona_id)
    if not target_user_persona:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    # Check for Persona with that name in dictionary table
    target_persona = Persona.query.filter(Persona.title_en == form.title.data.lower()).first()

    # If Persona does not exist in dictionary table create a new persona with target name
    if not target_persona:
        target_persona = Persona(title_en = form.title.data.lower())
        db.session.add(target_persona)
        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to update user persona - creating new persona failed", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_plan_home"))
    
    # Create updated User_Persona object with new id an description
    target_user_persona.active = form.active.data
    target_user_persona.user_id = g.user.id
    target_user_persona.persona_id = target_persona.id
    target_user_persona.description_private = form.description.data

    try:
        db.session.commit()
        return redirect(url_for("plan_bp.get_plan_home"))
    except Exception as e:
        flash("Error: Unable to update user persona - update action failed", "danger")
        print(e)
        db.session.rollback()  

# Delete Persona
@plan_bp.route("/persona/<int:persona_id>/delete", methods=["POST"])
@login_required
def delete_persona(persona_id):
     # Check that User Persona and User ID combo exists, if not unauthorized access
    target_user_persona = query_one_user_persona(g.user.id, persona_id)
    if not target_user_persona:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    db.session.delete(target_user_persona)
    try:
        db.session.commit()
    except Exception as e:
        flash("Error: Unable to delete user persona", "danger")
        print(e)
        db.session.rollback()  
    
    return redirect(url_for("plan_bp.get_plan_home"))

 
##########################
# CrUD - Habit Routes
##########################

# Create Habit
@plan_bp.route("/habit/new", methods=["GET"])
@login_required
def get_new_habit():
    # Create user habit form and fill Select choices from database
    form = UserHabitForm()

    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Reminder schedule is a future feature - Not implemented in the MVP version
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # user_habit_form.schedule_id.choices = reminder_schedule_list

    return render_template("plan_new_habit.html", user_habit_form=form)

@plan_bp.route("/habit/new", methods=["POST"])
@login_required
def add_user_habit():
    # Create user form and fill Select choices from database
    form = UserHabitForm(request.form)

    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Reminder schedule is a future feature - Not implemented in the MVP version
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # user_habit_form.schedule_id.choices = reminder_schedule_list

    # If form cannot be validated re-render page
    if not form.validate_on_submit():
        return render_template("plan_new_habit.html", user_habit_form=form)

    # If target habit does not exist in dictionary add new entry in the Habit table
    target_habit = Habit.query.filter(Habit.title_en == form.title.data.lower()).first()
    if not target_habit:
        target_habit = Habit(title_en = form.title.data.lower())
        db.session.add(target_habit)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new habit", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_new_habit"))

    # Find the id number for the selected target persona and create new User Habit entry
    target_persona = User_Persona.query.filter(User_Persona.id == form.persona.data).first()

    new_user_habit = User_Habit(
                        active = form.active.data, 
                        user_id = g.user.id, 
                        user_persona_id = target_persona.id, 
                        scoring_system_id = form.scoring_system_id.data, 
                        # schedule_id = schedule_id,
                        habit_id = target_habit.id, 
                        linked_goal_id = None,
                        description_private = form.description.data)

    db.session.add(new_user_habit)

    try:
        db.session.commit()
    except Exception as e:
        flash("Error: Unable to create new user habit", "danger")
        print(e)
        db.session.rollback()

    return redirect(url_for("plan_bp.get_plan_home"))

# Update Habit
@plan_bp.route("/habit/<int:habit_id>/edit", methods=["GET"])
@login_required
def get_edit_habit(habit_id):
    # Check that User Habit and User ID combo exists, if not unauthorized access
    target_user_habit = query_one_user_habit_dict_join(g.user.id, habit_id)
    if not target_user_habit:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    # Create form and populate the select fields with valid selection options
    form = UserHabitForm()

    # Retrieve & Create list of valid personas for the logged in user in Tuple Format (id, display_text)
    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    # Retrieve & Create list of valid scoring systems for the logged in user in Tuple Format (id, display_text)
    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Retrieve & Create list of valid reminder schedules for the logged in user in Tuple Format (id, display_text)
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # form.schedule_id.choices = reminder_schedule_list

    # Load data retrieved from the database into the form object for rendering
    form.title.data = target_user_habit.title_en
    form.description.data = target_user_habit.User_Habit.description_private
    form.persona.data = target_user_habit.User_Habit.user_persona_id
    form.scoring_system_id.data = target_user_habit.User_Habit.scoring_system_id
    # form.schedule_id.data = target_user_habit.User_Habit.schedule_id
    form.active.data = target_user_habit.User_Habit.active

    return render_template("plan_edit_habit.html",
            user_habit_form=form, habit_id=habit_id)

@plan_bp.route("/habit/<int:habit_id>/edit", methods=["POST"])
@login_required
def update_habit(habit_id):
    # Check that User Habit and User ID combo exists, if not unauthorized access
    target_user_habit = query_one_user_habit(g.user.id, habit_id)
    if not target_user_habit:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    form = UserHabitForm(request.form)

    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Reminder schedule is a future feature - Not implemented in the MVP version
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # user_habit_form.schedule_id.choices = reminder_schedule_list

    # If form cannot be validated re-render page
    if not form.validate_on_submit():
        return render_template("plan_edit_habit.html",
                            user_habit_form=form, habit_id=habit_id)

    # If target habit does not exist in dictionary add new entry in the Habit table
    target_habit = Habit.query.filter(Habit.title_en == form.title.data.lower()).first()
    if not target_habit:
        target_habit = Habit(title_en = form.title.data.lower())
        db.session.add(target_habit)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Failed to update user habit title", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_plan_home"))
    

    # Find the id number for the selected target persona and update User Habit entry
    target_persona = User_Persona.query.filter(User_Persona.id == form.persona.data).first()
    
    target_user_habit.active = form.active.data
    target_user_habit.user_persona_id = target_persona.id
    target_user_habit.scoring_system_id = form.scoring_system_id.data
    # target_user_habit.schedule_id = form.schedule_id.data
    target_user_habit.habit_id = target_habit.id
    target_user_habit.description_private = form.description.data

    try:
        db.session.commit()
        return redirect(url_for("plan_bp.get_plan_home"))
    except Exception as e:
        flash("Error: Unable to update user habit", "danger")
        print(e)
        db.session.rollback()
        return redirect(url_for("plan_bp.get_edit_habit")) 

# Delete Habit
@plan_bp.route("/habit/<int:habit_id>/delete", methods=["POST"])
@login_required
def delete_habit(habit_id):
    # Check that User Habit and User ID combo exists, if not unauthorized access
    target_user_habit = query_one_user_habit_dict_join(g.user.id, habit_id)
    if not target_user_habit:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    # Attempt to delete habit from the database
    db.session.delete(target_user_habit)
    try:
        db.session.commit()
    except Exception as e:
        flash("Error: Unable to delete user habit", "danger")
        print(e)
        db.session.rollback()  

    return redirect(url_for("plan_bp.get_plan_home"))


##########################
# CrUD - Goal Routes
##########################

# Create Goal
@plan_bp.route("/goal/new", methods=["GET"])
@login_required
def get_new_goal():
    # Create user goal form and fill Select choices from database
    form = UserGoalForm()

    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Reminder schedule is a future feature - Not implemented in the MVP version
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # user_habit_form.schedule_id.choices = reminder_schedule_list

    return render_template("plan_new_goal.html",
            user_goal_form=form)

@plan_bp.route("/goal/new", methods=["POST"])
@login_required
def add_user_goal():
    form = UserGoalForm(request.form)

    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Reminder schedule is a future feature - Not implemented in the MVP version
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # user_habit_form.schedule_id.choices = reminder_schedule_list

    # If form cannot be validated re-render page
    if not form.validate_on_submit():
        return render_template("plan_new_goal.html", user_goal_form=form)

    # If target goal does not exist in dictionary add new entry in the Goal table
    target_goal = Goal.query.filter(Goal.title_en == form.title.data.lower()).first()
    
    if not target_goal:
        target_goal = Goal(title_en = form.title.data.lower())
        db.session.add(target_goal)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new goal", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_new_goal"))

    # Find the id number for the selected target persona and create new User Goal entry
    target_persona = User_Persona.query.filter(User_Persona.id == form.persona.data).first()

    #!!!# The user should also be able to link a goal to a habit in the future
    new_user_goal = User_Goal(
                        active = form.active.data, 
                        user_id = g.user.id, 
                        user_persona_id = target_persona.id, 
                        scoring_system_id = form.scoring_system_id.data, 
                        # schedule_id = schedule_id,
                        goal_id = target_goal.id, 
                        description_private = form.description.data)

    db.session.add(new_user_goal)

    try:
        db.session.commit()
    except Exception as e:
        flash("Error: Unable to create new user goal", "danger")
        print(e)
        db.session.rollback()

    return redirect(url_for("plan_bp.get_plan_home"))

# Update Goal
@plan_bp.route("/goal/<int:goal_id>/edit", methods=["GET"])
@login_required
def get_edit_goal(goal_id):
    # Check that User Habit and User ID combo exists, if not unauthorized access
    target_user_goal = query_one_user_goal_dict_join(g.user.id, goal_id)
    if not target_user_goal:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    form = UserGoalForm()

    # Retrieve & Create list of valid personas for the logged in user in Tuple Format (id, display_text)
    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    # Retrieve & Create list of valid scoring systems for the logged in user in Tuple Format (id, display_text)
    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Retrieve & Create list of valid reminder schedules for the logged in user in Tuple Format (id, display_text)
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # form.schedule_id.choices = reminder_schedule_list    

    # Load data retrieved from the database into the form object for rendering
    form.title.data = target_user_goal.title_en
    form.description.data = target_user_goal.User_Goal.description_private
    form.persona.data = target_user_goal.User_Goal.user_persona_id
    form.scoring_system_id.data = target_user_goal.User_Goal.scoring_system_id
    # form.schedule_id.data = target_user_goal.User_Goal.schedule_id
    form.active.data = target_user_goal.User_Goal.active

    return render_template("plan_edit_goal.html",
            user_goal_form=form, goal_id=goal_id)

@plan_bp.route("/goal/<int:goal_id>/edit", methods=["POST"])
@login_required
def update_goal(goal_id):
    # Check that User Goal and User ID combo exists, if not unauthorized access
    target_user_goal = query_one_user_goal(g.user.id, goal_id)
    if not target_user_goal:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    form = UserGoalForm(request.form)

    user_personas = query_all_user_personas(g.user.id)
    persona_list = [(persona.User_Persona.id, persona.title_en) for persona in user_personas]
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    # Reminder schedule is a future feature - Not implemented in the MVP version
    # user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    # reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
    # user_habit_form.schedule_id.choices = reminder_schedule_list

    # If form cannot be validated re-render page
    if not form.validate_on_submit():
        return render_template("plan_edit_goal.html",
                            user_goal_form=form, goal_id=goal_id)

    # If target goal does not exist in dictionary add new entry in the Goal table
    target_goal = Goal.query.filter(Goal.title_en == form.title.data.lower()).first()
    if not target_goal:
        target_goal = Goal(title_en = form.title.data.lower())
        db.session.add(target_goal)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Failed to update user goal title", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_plan_home"))
    
    
    target_persona = User_Persona.query.filter(User_Persona.id == form.persona.data).first()
    
    target_user_goal.active = form.active.data
    target_user_goal.user_persona_id = target_persona.id
    target_user_goal.scoring_system_id = form.scoring_system_id.data
    # target_user_goal.schedule_id = form.schedule_id.data
    target_user_goal.goal_id = target_goal.id
    target_user_goal.description_private = form.description.data

    try:
        db.session.commit()
        return redirect(url_for("plan_bp.get_plan_home"))
    except Exception as e:
        flash("Error: Unable to update user goal", "danger")
        print(e)
        db.session.rollback()
        return redirect(url_for("plan_bp.get_edit_goal"))

# Delete Goal
@plan_bp.route("/goal/<int:goal_id>/delete", methods=["POST"])
@login_required
def delete_goal(goal_id):
    # Check that User Goal and User ID combo exists, if not unauthorized access
    target_user_goal = query_one_user_goal(g.user.id, goal_id)
    if not target_user_goal:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("plan_bp.get_plan_home"))

    # Attempt to delete goal from the database
    db.session.delete(target_user_goal)
    try:
        db.session.commit()
    except Exception as e:
        flash("Error: Unable to delete user goal", "danger")
        print(e)
        db.session.rollback()  

    return redirect(url_for("plan_bp.get_plan_home"))