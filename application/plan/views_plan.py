from flask import Blueprint, render_template, redirect, flash, request, session, g, url_for
from flask import current_app as app
from sqlalchemy import exc, or_, and_

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
            .outerjoin(User_Persona, User_Persona.id == User_Habit.user_persona_id)\
            .add_columns(User_Persona.id.label("persona_id"))\
            .outerjoin(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(Persona.title_en.label("persona_title"))\
            .filter(User_Habit.user_id == g.user.id).all()

        user_goals = User_Goal.query\
            .join(Goal, User_Goal.goal_id == Goal.id)\
            .add_columns(User_Goal.user_id, Goal.title_en, Goal.description_public)\
            .outerjoin(User_Persona, User_Persona.id == User_Goal.user_persona_id)\
            .add_columns(User_Persona.id.label("persona_id"))\
            .outerjoin(Persona, User_Persona.persona_id == Persona.id)\
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

##########################
# CrUD - Persona Routes
##########################

# Create Persona
@plan_bp.route("/persona/new", methods=["GET"])
def get_new_persona():
    if g.user:

        user_persona_form = UserPersonaFrom()

        return render_template("plan_new_persona.html",
                user_persona_form=user_persona_form)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@plan_bp.route("/persona/new", methods=["POST"])
def add_user_persona():
    form = UserPersonaFrom(request.form)

    if form.validate_on_submit():
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
            return redirect(url_for("plan_bp.get_new_persona"))

    return redirect(url_for("plan_bp.get_plan_home"))

# Update Persona
@plan_bp.route("/persona/<int:persona_id>/edit", methods=["GET"])
def get_edit_persona(persona_id):
    if g.user:

        target_persona = User_Persona.query\
            .join(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(User_Persona.user_id, Persona.title_en, Persona.description_public)\
            .filter(and_(User_Persona.user_id == g.user.id, User_Persona.id == persona_id)).first()

        if target_persona:
            user_persona_form = UserPersonaFrom(
                title = target_persona.title_en,
                description = target_persona.User_Persona.description_private,
                active = target_persona.User_Persona.active
            )

            return render_template("plan_edit_persona.html",
                    user_persona_form=user_persona_form, persona_id=persona_id)

        else:
            flash("We were unable to retrive your details for that persona.", "warning")
            return redirect(url_for("home_bp.homepage"))

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@plan_bp.route("/persona/<int:persona_id>/edit", methods=["POST"])
def update_persona(persona_id):
    if g.user:

        form = UserPersonaFrom(request.form)

        target_user_persona = User_Persona.query\
            .filter(and_(User_Persona.user_id == g.user.id, User_Persona.id == persona_id)).first()

        if target_user_persona and form.validate_on_submit():

            # Check for Persona with that name in dictionary table
            target_persona = Persona.query.filter(Persona.title_en == form.title.data.lower()).first()

            # If does not exist create a new persona under target name
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

        return render_template("plan_edit_persona.html",
                user_persona_form=form)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

# Delete Persona
@plan_bp.route("/persona/<int:persona_id>/delete", methods=["POST"])
def delete_persona(persona_id):
    if g.user:

        target_user_persona = User_Persona.query\
            .filter(and_(User_Persona.user_id == g.user.id, User_Persona.persona_id == persona_id)).first()

        if target_user_persona:
            db.session.delete(target_user_persona)

            try:
                db.session.commit()
            except Exception as e:
                flash("Error: Unable to delete user persona", "danger")
                print(e)
                db.session.rollback()  
        
        else:
            flash("You do not have appropriate permissions to delete that user persona.", "warning")    
        
        return redirect(url_for("plan_bp.get_plan_home"))

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))


##########################
# CrUD - Habit Routes
##########################

# Create Habit
@plan_bp.route("/habit/new", methods=["GET"])
def get_new_habit():
    if g.user:
        user_personas = User_Persona.query\
            .join(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(Persona.id, Persona.title_en)\
            .filter(User_Persona.user_id == g.user.id).all()

        persona_list = [(persona.id, persona.title_en) for persona in user_personas]

        user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
        scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]

        user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
        reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]
        

        user_habit_form = UserHabitForm()
        
        user_habit_form.persona.choices = persona_list
        user_habit_form.scoring_system_id.choices = scoring_system_list
        user_habit_form.schedule_id.choices = reminder_schedule_list

        return render_template("plan_new_habit.html",
                user_habit_form=user_habit_form)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@plan_bp.route("/habit/new", methods=["POST"])
def add_user_habit():
    form = UserHabitForm(request.form)

    user_personas = User_Persona.query.filter(User_Persona.user_id == g.user.id).all()
    persona_list = [(persona.persona_id, "p") for persona in user_personas] # This works becuase the validate_on_submit only checks the id (first) value of the tuple
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, "s") for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    reminder_schedule_list = [(schedule.id, "s") for schedule in user_reminder_schedule]
    form.schedule_id.choices = reminder_schedule_list


    if form.validate_on_submit():
        target_habit = Habit.query.filter(Habit.title_en == form.title.data.lower()).first()
        target_persona = Persona.query.filter(Persona.id == form.persona.data).first()

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
            
        active = form.active.data
        user_id = g.user.id
        persona_id = target_persona.id
        habit_id = target_habit.id
        scoring_system_id = form.scoring_system_id.data
        schedule_id = form.schedule_id.data

        new_user_habit = User_Habit(
                            active = active, 
                            user_id = user_id, 
                            user_persona_id = persona_id, 
                            scoring_system_id = scoring_system_id, 
                            schedule_id = schedule_id,
                            habit_id = habit_id, 
                            linked_goal_id = None,
                            description_private = form.description.data)

        db.session.add(new_user_habit)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new user habit", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_new_habit"))

    return redirect(url_for("plan_bp.get_plan_home"))

# Update Habit
@plan_bp.route("/habit/<int:habit_id>/edit", methods=["GET"])
def get_edit_habit(habit_id):
    if g.user:

        target_user_habit = User_Habit.query\
            .join(Habit, User_Habit.habit_id == Habit.id)\
            .add_columns(User_Habit.user_id, Habit.title_en, Habit.description_public)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id)).first()

        if target_user_habit:

            # Retrieve & Create list of valid personas for the logged in user in Tuple Format (id, display_text)
            user_personas = User_Persona.query\
                .join(Persona, User_Persona.persona_id == Persona.id)\
                .add_columns(Persona.id, Persona.title_en)\
                .filter(User_Persona.user_id == g.user.id).all()

            persona_list = [(persona.id, persona.title_en) for persona in user_personas]

            # Retrieve & Create list of valid scoring systems for the logged in user in Tuple Format (id, display_text)
            user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
            scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]

            # Retrieve & Create list of valid reminder schedules for the logged in user in Tuple Format (id, display_text)
            user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
            reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]

            # Create form and populate the select fields with valid selection options
            user_habit_form = UserHabitForm()
            
            user_habit_form.persona.choices = persona_list
            user_habit_form.scoring_system_id.choices = scoring_system_list
            user_habit_form.schedule_id.choices = reminder_schedule_list

            # Load data retrieved from the database into the form object for rendering
            user_habit_form.title.data = target_user_habit.title_en
            user_habit_form.description.data = target_user_habit.User_Habit.description_private
            user_habit_form.persona.data = target_user_habit.User_Habit.user_persona_id
            user_habit_form.scoring_system_id.data = target_user_habit.User_Habit.scoring_system_id
            user_habit_form.schedule_id.data = target_user_habit.User_Habit.schedule_id
            user_habit_form.active.data = target_user_habit.User_Habit.active


            return render_template("plan_edit_habit.html",
                    user_habit_form=user_habit_form, habit_id=habit_id)

        else:
            flash("We were unable to retrive your details for that habit.", "warning")

    else:
        flash("You must be logged in to access that page.", "warning")

    return redirect(url_for("plan_bp.get_plan_home"))

@plan_bp.route("/habit/<int:habit_id>/edit", methods=["POST"])
def update_habit(habit_id):
    if g.user:

        target_user_habit = User_Habit.query\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id)).first()

        if target_user_habit:

            form = UserHabitForm(request.form)

            # Retrieve & Create list of valid personas for the logged in user in Tuple Format (id, text)
            # Text is not being validated here, only id number is checked hense text is not dynamically loaded
            user_personas = User_Persona.query.filter(User_Persona.user_id == g.user.id).all()
            persona_list = [(persona.persona_id, "p") for persona in user_personas] # This works becuase the validate_on_submit only checks the id (first) value of the tuple
            form.persona.choices = persona_list

            # Retrieve & Create list of valid scoring systems for the logged in user in Tuple Format (id, text)
            # Text is not being validated here, only id number is checked hense text is not dynamically loaded
            user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
            scoring_system_list = [(system.id, "s") for system in user_scoring_systems]
            form.scoring_system_id.choices = scoring_system_list

            # Retrieve & Create list of valid reminder schedules for the logged in user in Tuple Format (id, text)
            # Text is not being validated here, only id number is checked hense text is not dynamically loaded
            user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
            reminder_schedule_list = [(schedule.id, "s") for schedule in user_reminder_schedule]
            form.schedule_id.choices = reminder_schedule_list

            if form.validate_on_submit():
                target_habit = Habit.query.filter(Habit.title_en == form.title.data.lower()).first()
                target_persona = Persona.query.filter(Persona.id == form.persona.data).first()

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
                
                
                target_user_habit.active = form.active.data
                target_user_habit.user_persona_id = target_persona.id
                target_user_habit.scoring_system_id = form.scoring_system_id.data
                target_user_habit.schedule_id = form.schedule_id.data
                target_user_habit.habit_id = target_habit.id
                target_user_habit.description_private = form.description.data

                try:
                    db.session.commit()
                except Exception as e:
                    flash("Error: Unable to create new user habit", "danger")
                    print(e)
                    db.session.rollback()
                    return redirect(url_for("plan_bp.get_new_habit"))

            return redirect(url_for("plan_bp.get_plan_home"))

        else:
            flash("You don't have permission to do that.", "warning")

    else:
        flash("You must be logged in to access that page.", "warning")

    return redirect(url_for("plan_bp.get_plan_home"))

# Delete Habit
@plan_bp.route("/habit/<int:habit_id>/delete", methods=["POST"])
def delete_habit(habit_id):
    return redirect(url_for("home_bp.homepage"))


##########################
# CrUD - Goal Routes
##########################

# Create Goal
@plan_bp.route("/goal/new", methods=["GET"])
def get_new_goal():
    if g.user:
        user_personas = User_Persona.query\
            .join(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(Persona.id, Persona.title_en)\
            .filter(User_Persona.user_id == g.user.id).all()

        persona_list = [(persona.id, persona.title_en) for persona in user_personas]

        user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
        scoring_system_list = [(system.id, system.title_en) for system in user_scoring_systems]

        user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
        reminder_schedule_list = [(schedule.id, schedule.title_en) for schedule in user_reminder_schedule]

        user_goal_form = UserGoalForm()
        user_goal_form.persona.choices = persona_list
        user_goal_form.scoring_system_id.choices = scoring_system_list
        user_goal_form.schedule_id.choices = reminder_schedule_list

        return render_template("plan_new_goal.html",
                user_goal_form=user_goal_form)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@plan_bp.route("/goal/new", methods=["POST"])
def add_user_goal():
    form = UserGoalForm(request.form)

    user_personas = User_Persona.query.filter(User_Persona.user_id == g.user.id).all()
    persona_list = [(persona.persona_id, "p") for persona in user_personas] # This works becuase the validate_on_submit only checks the id part of the tuple
    form.persona.choices = persona_list

    user_scoring_systems = Scoring_System.query.filter(or_(Scoring_System.user_id == g.user.id, Scoring_System.public == True)).all()
    scoring_system_list = [(system.id, "s") for system in user_scoring_systems]
    form.scoring_system_id.choices = scoring_system_list

    user_reminder_schedule = Reminder_Schedule.query.filter(or_(Reminder_Schedule.user_id == g.user.id, Reminder_Schedule.public == True)).all()
    reminder_schedule_list = [(schedule.id, "s") for schedule in user_reminder_schedule]
    form.schedule_id.choices = reminder_schedule_list

    if form.validate_on_submit():
        target_goal = Goal.query.filter(Goal.title_en == form.title.data.lower()).first()
        target_persona = Persona.query.filter(Persona.id == form.persona.data).first()

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
            
        active = form.active.data
        user_id = g.user.id
        persona_id = target_persona.id
        goal_id = target_goal.id
        scoring_system_id = form.scoring_system_id.data
        schedule_id = form.schedule_id.data


        #!!!# The user should also be able to link a goal to a habit in the future
        new_user_goal = User_Goal(
                            active = active, 
                            user_id = user_id, 
                            user_persona_id = persona_id, 
                            scoring_system_id = scoring_system_id, 
                            schedule_id = schedule_id,
                            goal_id = goal_id, 
                            description_private = form.description.data)

        db.session.add(new_user_goal)

        try:
            db.session.commit()
        except Exception as e:
            flash("Error: Unable to create new user goal", "danger")
            print(e)
            db.session.rollback()
            return redirect(url_for("plan_bp.get_new_goal"))

    return redirect(url_for("plan_bp.get_plan_home"))

# Update Goal
@plan_bp.route("/goal/<int:goal_id>/edit", methods=["GET"])
def get_edit_goal(goal_id):
    return redirect(url_for("home_bp.homepage"))

@plan_bp.route("/goal/<int:goal_id>/edit", methods=["POST"])
def update_goal(goal_id):
    return redirect(url_for("home_bp.homepage"))

# Delete Goal
@plan_bp.route("/goal/<int:goal_id>/delete", methods=["POST"])
def delete_goal(goal_id):
    return redirect(url_for("home_bp.homepage"))
