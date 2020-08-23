from flask import Blueprint, render_template, redirect, flash, request, session, g, jsonify, url_for
from flask import current_app as app
from sqlalchemy import exc, and_, desc, func
from .models.model_habit_score import Habit_Score
from .models.model_goal_score import Goal_Score
from .models.model_scoring_system import Scoring_System
from .models.model_scoring_system_params import Scoring_System_Params
from .models.model_reminder_schedule import Reminder_Schedule

from ..plan.models.model_user_persona import User_Persona
from ..plan.models.model_persona import Persona

from ..plan.models.model_user_habit import User_Habit
from ..plan.models.model_user_goal import User_Goal
from ..plan.models.model_goal import Goal
from ..plan.models.model_habit import Habit

from .forms.form_scoring_system import ScoringSystemForm
from .forms.form_scoring_param import ScoringSystemParamForm
from .forms.form_goal_score import GoalScoreForm
from .forms.form_habit_score import HabitScoreForm

from datetime import datetime, timedelta, date, timezone
from application import db
import gviz_api

# Blueprint Configuration
tracking_bp = Blueprint(
    'tracking_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

msg_not_logged_in = "Please login to continue."
msg_not_authorized = "You are not authorized to view that resource."


def query_one_scoring_sys(user_id, scoring_sys_id):
    query_result = Scoring_System.query\
            .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()
    return query_result

# def query_scoring_sys_params(user_id, scoring_sys_id):
#     query_result = Scoring_System.query\
#             .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
#             .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en,  Scoring_System_Params.id)\
#             .filter(and_(Scoring_System.user_id == user_id, Scoring_System.id == scoring_sys_id))\
#             .order_by(Scoring_System_Params.score_bp)\
#             .all()
#     return query_result

def query_scoring_sys_params(user_id, scoring_sys_id):
    query_result = Scoring_System_Params.query.filter(Scoring_System_Params.scoring_system_id == scoring_sys_id)
    return query_result


@tracking_bp.route("/", methods=["GET"])
def get_tracking_home():
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    scoring_systems = Scoring_System.query.filter(Scoring_System.user_id == g.user.id).all()

    # FUTURE: Implement button disable if there is an associated habit or goal
    # associated_habits = User_Habit.query\
    #     .filter(User_Habit.scoring_system_id == scoring_sys.id).all()

    # associated_goals = User_Goal.query\
    #     .filter(User_Goal.scoring_system_id == scoring_sys.id).all()

    return render_template("tracking_home.html", scoring_systems = scoring_systems)

################################
# CrUD - Scoring System Routes
################################

# Create Scoring System
@tracking_bp.route("/scoring_sys/new", methods=["GET"])
def get_new_scoring_sys():
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # Create form object for rendering
    form = ScoringSystemForm(request.form)
    return render_template("scoring_system_new.html", form = form)

@tracking_bp.route("/scoring_sys/new", methods=["POST"])
def add_new_scoring_sys():
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # Re-render page if unable to validate form data
    form = ScoringSystemForm(request.form)
    if not form.validate_on_submit():
        return render_template(url_for("tracking_bp.get_new_scoring_sys"), form=form)

    # If valid create scoring system object and try to add to database
    scoring_sys = Scoring_System(
        user_id = g.user.id,
        title_en = form.title.data,
        description = form.description.data,
        public = False
    )

    try:
        db.session.add(scoring_sys)
        db.session.commit()
        return redirect(url_for("tracking_bp.get_new_scoring_params", scoring_sys_id = scoring_sys.id))
    except Exception as e:
        flash("Sorry we ran into the problem!", "danger")
        print(e)
        db.session.rollback()

    # If exception occured redirect to tracking home
    return redirect(url_for("tracking_bp.get_tracking_home"))


# Update Scoring System
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/edit", methods=["GET"])
def get_edit_scoring_sys(scoring_sys_id):
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # Get scoring system
    scoring_sys = query_one_scoring_sys(g.user.id, scoring_sys_id)

    # If no scoring system found for user.id & scoring system combo access not authorized
    if not scoring_sys:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("tracking_bp.get_tracking_home"))

    # Render form with scoring system information
    form = ScoringSystemForm(
        title = scoring_sys.title_en,
        description = scoring_sys.description
    )

    return render_template("scoring_system_edit.html",
            form=form, scoring_sys=scoring_sys)

@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/edit", methods=["POST"])
def update_scoring_sys(scoring_sys_id):
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # If no scoring system found for user.id & scoring system combo access not authorized
    scoring_sys = query_one_scoring_sys(g.user.id, scoring_sys_id)
    if not scoring_sys:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("tracking_bp.get_tracking_home"))

    # Re-render page if unable to validate form data
    form = ScoringSystemForm(request.form)
    if not form.validate_on_submit():
        return render_template("scoring_system_edit.html",
                form=form, scoring_sys=scoring_sys)

    # If data ok update scoring_sys data with form data & commit
    scoring_sys.title_en = form.title.data
    scoring_sys.description = form.description.data

    try:
        db.session.commit()
        return redirect(url_for("tracking_bp.get_tracking_home"))
    except Exception as e:
        flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
        print(e)
        db.session.rollback()

    # Catch errant route paths & redirect to tracking home
    return redirect(url_for("tracking_bp.get_tracking_home"))


# Delete Scoring System
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/delete", methods=["POST"])
def delete_scoring_sys(scoring_sys_id):
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # If no scoring system found for user.id & scoring system combo access not authorized
    scoring_sys = query_one_scoring_sys(g.user.id, scoring_sys_id)
    if not scoring_sys:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("tracking_bp.get_tracking_home"))

    #  Check for associated habits or goals
    associated_habits = User_Habit.query\
        .filter(User_Habit.scoring_system_id == scoring_sys.id).all()

    associated_goals = User_Goal.query\
        .filter(User_Goal.scoring_system_id == scoring_sys.id).all()

    # If no habits or goals associated, ok to delete
    if not associated_habits and not associated_goals:
        db.session.delete(scoring_sys)
        try:
            db.session.commit()
        except Exception as e:
            flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
            print(e)
            db.session.rollback()
    else:
        flash("We were unable to delete this scoring system, please ensure no habits or goals are linked to this system.", "warning")

    # Redirect all outcomes to tracking hompage
    return redirect(url_for("tracking_bp.get_tracking_home"))


###################################
# CRUD - Scoring System Parameters
###################################

# Read Scoring System Parameters
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params", methods=["GET"])
def get_new_scoring_params(scoring_sys_id):
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # If no scoring system found for user.id & scoring system combo access not authorized
    scoring_sys = query_one_scoring_sys(g.user.id, scoring_sys_id)
    if not scoring_sys:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("tracking_bp.get_tracking_home"))

    # Load all parameters for the target scoring system
    parameters = query_scoring_sys_params(g.user.id, scoring_sys.id)

    # Create form object for rendering
    form = ScoringSystemParamForm(request.form)
    return render_template("scoring_system_params.html", form = form, scoring_system = scoring_sys, parameters = parameters)

# Create New Scoring System Parameter
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/new", methods=["POST"])
def add_new_scoring_param(scoring_sys_id):
    # Check for login
    if not g.user:
        flash(msg_not_logged_in, "warning")
        return redirect(url_for("home_bp.homepage"))

    # If no scoring system found for user.id & scoring system combo access not authorized
    scoring_sys = query_one_scoring_sys(g.user.id, scoring_sys_id)
    if not scoring_sys:
        flash(msg_not_authorized, "warning")
        return redirect(url_for("tracking_bp.get_tracking_home"))

    # Load all parameters for the target scoring system
    parameters = query_scoring_sys_params(g.user.id, scoring_sys.id)

    # Re-render page if unable to validate form data
    form = ScoringSystemParamForm(request.form)
    if not form.validate_on_submit():
        return render_template("scoring_system_params.html", form = form, scoring_system = scoring_sys, parameters = parameters)

    # If form data valid calculate next score_bp (score breakpoint) value
    breakpoints = [param.score_bp for param in parameters]

    if breakpoints:
        score_bp = max(breakpoints) + 1
    else:
        score_bp = 1

    # Creating scoring system parameter object and try to add to database
    param = Scoring_System_Params(
        scoring_system_id = scoring_sys_id,
        score_bp = score_bp,
        score_input = form.score_input.data,
        score_output = form.score_output.data,
        name_en = form.name_en.data
    )

    try:
        db.session.add(param)
        db.session.commit()    
    except Exception as e:
        flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
        print(e)
        db.session.rollback()

    # Redirect all outcomes to scoring system parameters page
    return redirect(url_for("tracking_bp.get_new_scoring_params", scoring_sys_id = scoring_sys_id))

# !!!!!!!!!!!!!!!!!!!!!!!!!!!
# REWORKED TO HERE - 08/23/2020
# !!!!!!!!!!!!!!!!!!!!!!!!!!!
# Update Scoring System Parameter
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/<int:scoring_param_id>/edit", methods=["GET"])
def get_edit_scoring_param(scoring_sys_id, scoring_param_id):
    if g.user:

        scoring_system = Scoring_System.query.filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()

        if scoring_system:
            parameters = Scoring_System.query\
                .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
                .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en,  Scoring_System_Params.id)\
                .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id))\
                .order_by(Scoring_System_Params.score_bp)\
                .all()


            system_parameter = Scoring_System_Params.query.filter(and_(Scoring_System_Params.scoring_system_id == scoring_system.id, Scoring_System_Params.id == scoring_param_id)).first()

            if system_parameter:

                form = ScoringSystemParamForm(
                    score_input = system_parameter.score_input,
                    score_output = system_parameter.score_output,
                    name_en = system_parameter.name_en
                )

                return render_template("scoring_system_params.html",
                        form=form, scoring_system=scoring_system, parameters=parameters, edit=True, scoring_param_id=system_parameter.id)
            else:
                flash("We were unable to retrive your details for that scoring system parameter.", "warning")
        
        else:
            flash("We were unable to retrieve that scoring system for your account.", "warning")

        return redirect(url_for("tracking_bp.get_tracking_home"))

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  

@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/<int:scoring_param_id>/edit", methods=["POST"])
def update_scoring_param(scoring_sys_id, scoring_param_id):
    if g.user:

        scoring_system = Scoring_System.query.filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()

        parameters = Scoring_System.query\
            .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
            .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en,  Scoring_System_Params.id)\
            .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id))\
            .order_by(Scoring_System_Params.score_bp)\
            .all()


        form = ScoringSystemParamForm(request.form)

        if scoring_system and form.validate_on_submit():
            system_parameter = Scoring_System_Params.query.filter(and_(Scoring_System_Params.scoring_system_id == scoring_system.id, Scoring_System_Params.id == scoring_param_id)).first()

            if system_parameter:
                system_parameter.score_input = form.score_input.data
                system_parameter.score_output = form.score_output.data
                system_parameter.name_en = form.name_en.data

                try:
                    db.session.commit()
                    return redirect(url_for("tracking_bp.get_new_scoring_params", scoring_sys_id = scoring_system.id))
                except Exception as e:
                    flash("An error occured, if this problem persists please contact support", "danger")
                    print(e)
                    db.session.rollback()
            else:
                flash("We were unable to update the scoring system parameter.", "warning")

        return render_template("scoring_system_params.html",
                form=form, scoring_system=scoring_system, parameters=parameters, edit=True)      

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  

# Delete Scoring System Parameter
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/<int:scoring_param_id>/delete", methods=["POST"])
def delete_scoring_param(scoring_sys_id, scoring_param_id):
    if g.user:
        scoring_system = Scoring_System.query.filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()
        
        if scoring_system:
            system_parameter = Scoring_System_Params.query.filter(and_(Scoring_System_Params.scoring_system_id == scoring_system.id, Scoring_System_Params.id == scoring_param_id)).first()

            if system_parameter:
                db.session.delete(system_parameter)

                try:
                    db.session.commit()
                except Exception as e:
                    flash("An error occured, if this problem persists please contact support", "danger")
                    print(e)
                    db.session.rollback()
            else:
                flash("We were unable to find the target system parameter.", "warning")

        else:
            flash("We were unable to find the target scoring system.", "warning")

        return redirect(url_for("tracking_bp.get_new_scoring_params", scoring_sys_id = scoring_system.id))

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  


###################################
# CRUD - Goal Scores
###################################

# Create New Goal Score
@tracking_bp.route("/goal_scores/<int:goal_id>/new", methods=["GET"])
def get_new_goal_score(goal_id):
    if g.user:
        form = GoalScoreForm()

        user_goal = User_Goal.query\
            .join(Goal, Goal.id == User_Goal.goal_id)\
            .add_columns(Goal.title_en, Goal.description_public)\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id))\
            .first()
        
        goal_scores = Goal_Score.query\
            .filter(Goal_Score.goal_id == goal_id)\
            .order_by(desc(Goal_Score.date))\
            .all()

        form.date.data = datetime.today()

        return render_template("goal_score_new.html", form = form, user_goal = user_goal, goal_scores = goal_scores)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@tracking_bp.route("/goal_scores/<int:goal_id>/new", methods=["POST"])
def add_new_goal_score(goal_id):
    if g.user:
        form = GoalScoreForm(obj=request.form)

        user_goal = User_Goal.query\
            .join(Goal, Goal.id == User_Goal.goal_id)\
            .add_columns(Goal.title_en, Goal.description_public)\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id))\
            .first()

        if user_goal and form.validate_on_submit():

            date_check = Goal_Score.query\
                .join(User_Goal, User_Goal.id == Goal_Score.goal_id)\
                .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id, Goal_Score.date == form.date.data))\
                .first()

            if not date_check:

                score = Goal_Score(
                    date = form.date.data,
                    score = form.score.data,
                    goal_id = goal_id
                )

                # Try adding goal score to database
                try:
                    db.session.add(score)
                    db.session.commit()    
                except Exception as e:
                    flash("Oops... We were unable to add a new entry to your progress log.  We'll look into it!", "danger")
                    print(e)
                    db.session.rollback()
            
            else:
                flash("An entry already exists for this date, please modify existing entry.", "info")
                db.session.rollback()


            return redirect(url_for("tracking_bp.get_new_goal_score", goal_id = goal_id))

        else:
            return render_template("goal_score_new.html", form = form, user_goal = user_goal)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

# Update Goal Score
@tracking_bp.route("/goal_scores/<int:goal_id>/scores/<int:score_id>/update", methods=["GET"])
def get_edit_goal_score(goal_id, score_id):
    if g.user:

        user_goal = User_Goal.query\
            .join(Goal, Goal.id == User_Goal.goal_id)\
            .add_columns(Goal.title_en, Goal.description_public)\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id))\
            .first()

        if user_goal:
            goal_scores = Goal_Score.query\
                .filter(Goal_Score.goal_id == goal_id)\
                .order_by(desc(Goal_Score.date))\
                .all()

            target_score = Goal_Score.query\
                .filter(Goal_Score.id == score_id)\
                .first()

            form = GoalScoreForm(
                date = target_score.date,
                score = target_score.score
            )

            return render_template("goal_score_new.html", form = form, user_goal = user_goal, goal_scores = goal_scores, edit = True, target_score_id = target_score.id)

        else:
            flash("We were unable to retrieve the requested goal.", "warning")
            return redirect(url_for("plan_bp.get_plan_home"))

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@tracking_bp.route("/goal_scores/<int:goal_id>/scores/<int:score_id>/update", methods=["POST"])
def update_goal_score(goal_id, score_id):
    if g.user:
        form = GoalScoreForm(obj=request.form)

        user_goal = User_Goal.query\
            .join(Goal, Goal.id == User_Goal.goal_id)\
            .add_columns(Goal.title_en, Goal.description_public)\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id))\
            .first()

        goal_scores = Goal_Score.query\
            .filter(Goal_Score.goal_id == goal_id)\
            .order_by(desc(Goal_Score.date))\
            .all()

        if user_goal and form.validate_on_submit():

            date_check = Goal_Score.query\
                .join(User_Goal, User_Goal.id == Goal_Score.goal_id)\
                .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id, Goal_Score.date == form.date.data))\
                .first()

            if not date_check or date_check.id == score_id:
                target_score = Goal_Score.query\
                    .filter(Goal_Score.id == score_id)\
                    .first()

                target_score.date = form.date.data
                target_score.score = form.score.data

                # Try adding goal score to database
                try:
                    db.session.commit()    
                except Exception as e:
                    flash("Oops... We were unable to update this goal.  We're looking into it!", "danger")
                    print(e)
                    db.session.rollback()

                return redirect(url_for("tracking_bp.get_new_goal_score", goal_id = goal_id))
            
            else:
                flash("An entry already exists for the target date.", "info")
                db.session.rollback()
                return render_template("goal_score_new.html", form = form, user_goal = user_goal, goal_scores = goal_scores, edit = True)

        else:
            return render_template("goal_score_new.html", form = form, user_goal = user_goal, goal_scores = goal_scores, edit = True)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

# Delete Goal Score
@tracking_bp.route("/goal_scores/<int:goal_id>/scores/<int:score_id>/delete", methods=["POST"])
def delete_goal_score(goal_id, score_id):
    if g.user:

        user_goal = User_Goal.query\
            .join(Goal, Goal.id == User_Goal.goal_id)\
            .add_columns(Goal.title_en, Goal.description_public)\
            .join(Goal_Score, Goal_Score.goal_id == User_Goal.goal_id)\
            .add_columns(Goal_Score.id)\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id, Goal_Score.id == score_id))\
            .first()

        if user_goal:
            target_score = Goal_Score.query\
                .filter(Goal_Score.id == score_id)\
                .first()

            db.session.delete(target_score)

            try:
                db.session.commit()
            except Exception as e:
                flash("An error occured, if this problem persists please contact support", "danger")
                print(e)
                db.session.rollback()
        else:
            flash("We were unable to find the target score.", "warning")

        return redirect(url_for("tracking_bp.get_new_goal_score", goal_id = goal_id))

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  

###################################
# CRUD - Habit Scores
###################################

# Create New Habit Score
@tracking_bp.route("/habit_scores/<habit_id>/new", methods=["GET"])
def get_new_habit_score(habit_id):
    if g.user:
        form = HabitScoreForm()

        user_habit = User_Habit.query\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .add_columns(Habit.title_en, Habit.description_public)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id))\
            .first()
        
        habit_scores = Habit_Score.query\
            .filter(Habit_Score.habit_id == habit_id)\
            .order_by(desc(Habit_Score.date))\
            .all()

        form.date.data = datetime.today()

        return render_template("habit_score_new.html", form = form, user_habit = user_habit, habit_scores = habit_scores)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@tracking_bp.route("/habit_scores/<int:habit_id>/new", methods=["POST"])
def add_new_habit_score(habit_id):
    if g.user:
        form = HabitScoreForm(obj=request.form)

        user_habit = User_Habit.query\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .add_columns(Habit.title_en, Habit.description_public)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id))\
            .first()

        if user_habit and form.validate_on_submit():

            date_check = Habit_Score.query\
                .join(User_Habit, User_Habit.id == Habit_Score.habit_id)\
                .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id, Habit_Score.date == form.date.data))\
                .first()

            if not date_check:

                score = Habit_Score(
                    date = form.date.data,
                    score = form.score.data,
                    habit_id = habit_id
                )

                # Try adding habit score to database
                try:
                    db.session.add(score)
                    db.session.commit()    
                except Exception as e:
                    flash("Oops... We were unable to add a new entry to your progress log.  We'll look into it!", "danger")
                    print(e)
                    db.session.rollback()
            
            else:
                flash("An entry already exists for this date, please modify existing entry.", "info")
                db.session.rollback()


            return redirect(url_for("tracking_bp.get_new_habit_score", habit_id = habit_id))

        else:

            return render_template("habit_score_new.html", form = form, user_habit = user_habit)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

# Update Habit Score
@tracking_bp.route("/habit_scores/<int:habit_id>/scores/<int:score_id>/update", methods=["GET"])
def get_edit_habit_score(habit_id, score_id):
    if g.user:

        user_habit = User_Habit.query\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .add_columns(Habit.title_en, Habit.description_public)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id))\
            .first()

        if user_habit:
            habit_scores = Habit_Score.query\
                .filter(Habit_Score.habit_id == habit_id)\
                .order_by(desc(Habit_Score.date))\
                .all()

            target_score = Habit_Score.query\
                .filter(Habit_Score.id == score_id)\
                .first()

            form = HabitScoreForm(
                date = target_score.date,
                score = target_score.score
            )

            return render_template("habit_score_new.html", form = form, user_habit = user_habit, habit_scores = habit_scores, edit = True, target_score_id = target_score.id)

        else:
            flash("We were unable to retrieve the requested goal.", "warning")
            return redirect(url_for("plan_bp.get_plan_home"))

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@tracking_bp.route("/habit_scores/<int:habit_id>/scores/<int:score_id>/update", methods=["POST"])
def update_habit_score(habit_id, score_id):
    if g.user:
        form = HabitScoreForm(obj=request.form)

        user_habit = User_Habit.query\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .add_columns(Habit.title_en, Habit.description_public)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id))\
            .first()

        habit_scores = Habit_Score.query\
            .filter(Habit_Score.habit_id == habit_id)\
            .order_by(desc(Habit_Score.date))\
            .all()

        if user_habit and form.validate_on_submit():

            date_check = Habit_Score.query\
                .join(User_Habit, User_Habit.id == Habit_Score.habit_id)\
                .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id, Habit_Score.date == form.date.data))\
                .first()

            if not date_check or date_check.id == score_id:
                target_score = Habit_Score.query\
                    .filter(Habit_Score.id == score_id)\
                    .first()

                target_score.date = form.date.data
                target_score.score = form.score.data

                # Try adding habit score to database
                try:
                    db.session.commit()    
                except Exception as e:
                    flash("Oops... We were unable to update this habit.  We're looking into it!", "danger")
                    print(e)
                    db.session.rollback()

                return redirect(url_for("tracking_bp.get_new_habit_score", habit_id = habit_id))
            
            else:
                flash("An entry already exists for the target date.", "info")
                db.session.rollback()
                return render_template("habit_score_new.html", form = form, user_habit = user_habit, habit_scores = habit_scores, edit = True)

        else:
            return render_template("habit_score_new.html", form = form, user_habit = user_habit, habit_scores = habit_scores, edit = True)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

# Delete Habit Score
@tracking_bp.route("/habit_scores/<int:habit_id>/scores/<int:score_id>/delete", methods=["POST"])
def delete_habit_score(habit_id, score_id):
    if g.user:

        user_habit = User_Habit.query\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .add_columns(Habit.title_en, Habit.description_public)\
            .join(Habit_Score, Habit_Score.habit_id == User_Habit.habit_id)\
            .add_columns(Habit_Score.id)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id, Habit_Score.id == score_id))\
            .first()

        if user_habit:
            target_score = Habit_Score.query\
                .filter(Habit_Score.id == score_id)\
                .first()

            db.session.delete(target_score)

            try:
                db.session.commit()
            except Exception as e:
                flash("An error occured, if this problem persists please contact support", "danger")
                print(e)
                db.session.rollback()
        else:
            flash("We were unable to find the target score.", "warning")

        return redirect(url_for("tracking_bp.get_new_habit_score", habit_id = habit_id))

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  



###################################
# API Calls
###################################

@tracking_bp.route("/scoring_sys")
def get_scoring_sys():
    if g.user:

        system = request.args.get('system')

        system_parameters = Scoring_System.query\
                .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
                .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en)\
                .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == system)).all()

        description = {
            "time_input":   ("number", "Time Spent"),
            "score_output": ("number", "Score"),
            "score_label":  ("string",'',{'role':'tooltip'}),
            "score_order":  ("number",'Order',{'role':'annotation'})
            }

        data = []

        for param in system_parameters:
            data_point = {
                    "time_input": param.score_input,
                    "score_output": param.score_output,
                    "score_label": param.name_en,
                    "score_order": param.score_bp
                }
            data.append(data_point)


        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)

        # jsonResponse = data_table.ToJSonResponse(columns_order=("time_input", "score_output", "score_label", "score_order"),
        #                             order_by="score_order")

        jsonResponse = data_table.ToJSon(columns_order=("time_input", "score_output", "score_label", "score_order"),
                                    order_by="score_order")

        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse

@tracking_bp.route("/user_habit_scores")
def get_user_habit_scores():
    if g.user:

        habit_id = request.args.get('habit_id')
        qty_days = int(request.args.get('qty_days'))
        
        filter_after = datetime.now(timezone.utc) - timedelta(days = qty_days)

        score_results = User_Habit.query\
            .join(Habit_Score, User_Habit.id == Habit_Score.habit_id)\
            .add_columns(Habit_Score.date, Habit_Score.score)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id, Habit_Score.date >= filter_after))\
            .order_by(Habit_Score.date)\
            .all()

        target_habit = User_Habit.query\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id))\
            .first()

        scoring_system_parameters = Scoring_System.query\
            .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
            .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en)\
            .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == target_habit.scoring_system_id))\
            .order_by(Scoring_System_Params.score_bp)\
            .all()

        saved_dates = [result.date.date() for result in score_results]
        filled_score_results = []
        

        for day_offset in range(qty_days):
            search_date = filter_after + timedelta(days = day_offset)

            if search_date.date() in saved_dates:
                for result in score_results:
                    if search_date.date() == result.date.date():
                        data_point = {
                            "date": result.date,
                            "score": result.score
                        }
                        filled_score_results.append(data_point)
            else:
                data_point = {
                    "date": search_date,
                    "score": 0
                }
                filled_score_results.append(data_point)

        description = {
            "date":   ("datetime", "Time Spent"),
            "score": ("number", "Score"),
            "score_label":  ("string",'',{'role':'tooltip'})
            }        

        data = []

        len_param_list = len(scoring_system_parameters)

        for result in filled_score_results:
            data_point = {
                "date": result.get('date'),
                "score": None,
                "score_label": None
            }

            for idx, param in enumerate(scoring_system_parameters):
                if result.get('score') <= scoring_system_parameters[idx].score_input:
                    data_point["score"] = param.score_output
                    data_point["score_label"] = param.name_en
                    break
                elif result.get('score') > scoring_system_parameters[idx].score_input and idx == (len_param_list - 1):
                    data_point["score"] = param.score_output
                    data_point["score_label"] = param.name_en
                    break
                else:
                    continue        

            data.append(data_point)


        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)


        jsonResponse = data_table.ToJSon(columns_order=("date", "score", "score_label"),
                                    order_by="date")

        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse

@tracking_bp.route("/user_goal_scores")
def get_user_goal_scores():
    if g.user:

        goal_id = request.args.get('goal_id')
        qty_days = int(request.args.get('qty_days'))
        

        filter_after = datetime.now(timezone.utc) - timedelta(days = qty_days)

        score_results = User_Goal.query\
            .join(Goal_Score, User_Goal.id == Goal_Score.goal_id)\
            .add_columns(Goal_Score.date, Goal_Score.score)\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id, Goal_Score.date >= filter_after))\
            .order_by(Goal_Score.date)\
            .all()

        target_goal = User_Goal.query\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id))\
            .first()

        scoring_system_parameters = Scoring_System.query\
            .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
            .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en)\
            .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == target_goal.scoring_system_id))\
            .order_by(Scoring_System_Params.score_bp)\
            .all()

        saved_dates = [result.date.date() for result in score_results]
        filled_score_results = []
        
        for day_offset in range(qty_days):
            search_date = filter_after + timedelta(days = day_offset)

            if search_date.date() in saved_dates:
                for result in score_results:
                    if search_date.date() == result.date.date():
                        data_point = {
                            "date": result.date,
                            "score": result.score
                        }
                        filled_score_results.append(data_point)
            else:
                data_point = {
                    "date": search_date,
                    "score": 0
                }
                filled_score_results.append(data_point)

        description = {
            "date":   ("datetime", "Time Spent"),
            "score": ("number", "Score"),
            "score_label":  ("string",'',{'role':'tooltip'})
            }        

        data = []

        len_param_list = len(scoring_system_parameters)

        for result in filled_score_results:
            data_point = {
                "date": result.get('date'),
                "score": None,
                "score_label": None
            }

            for idx, param in enumerate(scoring_system_parameters):
                if result.get('score') <= scoring_system_parameters[idx].score_input:
                    data_point["score"] = param.score_output
                    data_point["score_label"] = param.name_en
                    break
                elif result.get('score') > scoring_system_parameters[idx].score_input and idx == (len_param_list - 1):
                    data_point["score"] = param.score_output
                    data_point["score_label"] = param.name_en
                    break
                else:
                    continue        

            data.append(data_point)


        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)


        jsonResponse = data_table.ToJSon(columns_order=("date", "score", "score_label"),
                                    order_by="date")


        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse


def calc_output_score(scoring_system_parameters, score):
    len_param_list = len(scoring_system_parameters)

    for idx, param in enumerate(scoring_system_parameters):
        if score <= scoring_system_parameters[idx].score_input:
            output = param.score_output
            break
        elif score > scoring_system_parameters[idx].score_input and idx == (len_param_list - 1):
            output = param.score_output
            break
        else:
            continue 

    return output

@tracking_bp.route("/api/persona_scores")
def get_user_persona_scores():
    if g.user:

        user_persona_id = request.args.get('user_persona_id')
        qty_days = int(request.args.get('qty_days'))

        filter_after = datetime.now(timezone.utc) - timedelta(days = qty_days)

        target_persona = User_Persona.query\
            .join(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(Persona.title_en)\
            .filter(and_(User_Persona.id == user_persona_id, User_Persona.user_id == g.user.id)).first()

        if not target_persona:
            jsonResponse = {'error': 'We were unable to locate data per your request.'}
            return jsonResponse

        active_habits = User_Persona.query\
            .join(User_Habit, User_Habit.user_persona_id == User_Persona.id)\
            .add_columns(User_Habit.id, User_Habit.active, User_Habit.scoring_system_id)\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .add_columns(Habit.title_en)\
            .filter(and_(User_Persona.id == user_persona_id, User_Persona.user_id == g.user.id, User_Habit.active == True))\
            .order_by(User_Habit.id)\
            .all()


        active_goals = User_Persona.query\
            .join(User_Goal, User_Goal.user_persona_id == User_Persona.id)\
            .add_columns(User_Goal.id, User_Goal.active, User_Goal.scoring_system_id)\
            .join(Goal, Goal.id == User_Goal.goal_id)\
            .add_columns(Goal.title_en)\
            .filter(and_(User_Persona.id == user_persona_id, User_Persona.user_id == g.user.id, User_Goal.active == True))\
            .order_by(User_Goal.id)\
            .all()

        

        data_entries = []

        for day_offset in range(qty_days):
            data_array = [filter_after + timedelta(day_offset)]
            data_entries.append(data_array)


        column_desc = [('Date', 'datetime')]

        for habit in active_habits:
            column_desc.append((habit.title_en, 'number'))

            score_results = User_Habit.query\
                .join(Habit_Score, User_Habit.id == Habit_Score.habit_id)\
                .add_columns(Habit_Score.date, Habit_Score.score)\
                .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit.id, Habit_Score.date >= filter_after))\
                .order_by(Habit_Score.date)\
                .all()

            scoring_system_parameters = Scoring_System.query\
                .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
                .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en)\
                .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == habit.scoring_system_id))\
                .order_by(Scoring_System_Params.score_bp)\
                .all()            

            for entry in data_entries:
                result_found = False

                for score in score_results:
                    if entry[0].date() == score.date.date():
                        result_found = True
                        entry.append(calc_output_score(scoring_system_parameters, score.score))

                if not result_found:
                    entry.append(0.0)


        for goal in active_goals:
            column_desc.append((goal.title_en, 'number'))

            score_results = User_Goal.query\
                .join(Goal_Score, User_Goal.id == Goal_Score.goal_id)\
                .add_columns(Goal_Score.date, Goal_Score.score)\
                .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal.id, Goal_Score.date >= filter_after))\
                .order_by(Goal_Score.date)\
                .all()

            scoring_system_parameters = Scoring_System.query\
                .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
                .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en)\
                .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == goal.scoring_system_id))\
                .order_by(Scoring_System_Params.score_bp)\
                .all()            

            for entry in data_entries:
                result_found = False

                for score in score_results:
                    if entry[0].date() == score.date.date():
                        result_found = True
                        entry.append(calc_output_score(scoring_system_parameters, score.score))

                if not result_found:
                    entry.append(0.0)

        data_table = gviz_api.DataTable(column_desc)
        data_table.AppendData(data_entries)

        jsonResponse = data_table.ToJSon()

        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse


@tracking_bp.route("/api/persona_scores_total_mins")
def get_user_persona_scores_total_mins():
    if g.user:

        user_persona_id = request.args.get('user_persona_id')

        target_persona = User_Persona.query\
            .join(Persona, User_Persona.persona_id == Persona.id)\
            .add_columns(Persona.title_en)\
            .filter(and_(User_Persona.id == user_persona_id, User_Persona.user_id == g.user.id)).first()

        if not target_persona:
            jsonResponse = {'error': 'We were unable to locate data per your request.'}
            return jsonResponse

        consolidated_habits = User_Persona.query\
            .with_entities(User_Persona.id, func.sum(Habit_Score.score))\
            .join(User_Habit, User_Habit.user_persona_id == User_Persona.id)\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .join(Habit_Score, Habit_Score.habit_id == User_Habit.id)\
            .group_by(User_Persona.id)\
            .filter(and_(User_Persona.id == user_persona_id, User_Persona.user_id == g.user.id))\
            .all()
        
        consolidated_goals = User_Persona.query\
            .with_entities(User_Persona.id, func.sum(Goal_Score.score))\
            .join(User_Goal, User_Goal.user_persona_id == User_Persona.id)\
            .join(Goal, Goal.id == User_Goal.goal_id)\
            .join(Goal_Score, Goal_Score.goal_id == User_Goal.id)\
            .group_by(User_Persona.id)\
            .filter(and_(User_Persona.id == user_persona_id, User_Persona.user_id == g.user.id))\
            .all()

        total_mins = 0

        if consolidated_goals and consolidated_habits:
            total_mins = consolidated_habits[0][1] + consolidated_goals[0][1]
        elif consolidated_habits:
            total_mins = consolidated_habits[0][1]
        elif consolidated_goals:
            total_mins = consolidated_goals[0][1]

        jsonResponse = {'total_mins': total_mins}

        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse