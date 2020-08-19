from flask import Blueprint, render_template, redirect, flash, request, session, g, jsonify, url_for
from flask import current_app as app
from sqlalchemy import exc, and_
from .models.model_habit_score import Habit_Score
from .models.model_goal_score import Goal_Score
from .models.model_scoring_system import Scoring_System
from .models.model_scoring_system_params import Scoring_System_Params
from .models.model_reminder_schedule import Reminder_Schedule

from ..plan.models.model_user_habit import User_Habit
from ..plan.models.model_user_goal import User_Goal
from ..plan.models.model_goal import Goal
from ..plan.models.model_habit import Habit

from .forms.form_scoring_system import ScoringSystemForm
from .forms.form_scoring_param import ScoringSystemParamForm
from .forms.form_goal_score import GoalScoreForm
from .forms.form_habit_score import HabitScoreForm

from datetime import datetime, timedelta
from application import db
import gviz_api

# Blueprint Configuration
tracking_bp = Blueprint(
    'tracking_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# TODO: Implement routes
@tracking_bp.route("/", methods=["GET"])
def get_tracking_home():

    if g.user:
        scoring_systems = Scoring_System.query.filter(Scoring_System.user_id == g.user.id).all()

        # TODO: Implement button disable if there is an associated habit or goal
        # associated_habits = User_Habit.query\
        #     .filter(User_Habit.scoring_system_id == scoring_sys.id).all()

        # associated_goals = User_Goal.query\
        #     .filter(User_Goal.scoring_system_id == scoring_sys.id).all()

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))

    return render_template("tracking_home.html", scoring_systems = scoring_systems)

################################
# CrUD - Scoring System Routes
################################

# Create Scoring System
@tracking_bp.route("/scoring_sys/new", methods=["GET"])
def get_new_scoring_sys():
    if g.user:
        form = ScoringSystemForm(request.form)

        return render_template("scoring_system_new.html", form = form)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

@tracking_bp.route("/scoring_sys/new", methods=["POST"])
def add_new_scoring_sys():
    if g.user:
        form = ScoringSystemForm(request.form)

        if form.validate_on_submit():
            scoring_sys = Scoring_System(
                user_id = g.user.id,
                title_en = form.title.data,
                description = form.description.data,
                public = False
            )

            # Try adding scoring system to database
            try:
                db.session.add(scoring_sys)
                db.session.commit()
                return redirect(url_for("tracking_bp.get_new_scoring_params", scoring_sys_id = scoring_sys.id))
            except Exception as e:
                flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
                print(e)
                db.session.rollback()

        else:
            return render_template(url_for("tracking_bp.get_new_scoring_sys"), form=form)

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  

# Update Scoring System
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/edit", methods=["GET"])
def get_edit_scoring_sys(scoring_sys_id):
    if g.user:

        scoring_sys = Scoring_System.query\
            .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()

        if scoring_sys:
            form = ScoringSystemForm(
                title = scoring_sys.title_en,
                description = scoring_sys.description
            )

            return render_template("scoring_system_edit.html",
                    form=form, scoring_sys=scoring_sys)
        else:
            flash("We were unable to retrive your details for that scoring system.", "warning")
            return redirect(url_for("home_bp.homepage"))

    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  

@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/edit", methods=["POST"])
def update_scoring_sys(scoring_sys_id):
    if g.user:
        scoring_sys = Scoring_System.query\
            .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()

        if scoring_sys:
            form = ScoringSystemForm(request.form)
            if form.validate_on_submit():
                scoring_sys.title_en = form.title.data
                scoring_sys.description = form.description.data

                try:
                    db.session.commit()
                    return redirect(url_for("tracking_bp.get_tracking_home"))
                except Exception as e:
                    flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
                    print(e)
                    db.session.rollback()
            else:
                return render_template("scoring_system_edit.html",
                        form=form, scoring_sys=scoring_sys)
        else:
            flash("We were unable to retrive your details for that scoring system.", "warning")
            return redirect(url_for("tracking_bp.get_tracking_home"))
    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  

    return redirect(url_for("tracking_bp.get_new_scoring_sys"))


# Delete Scoring System
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/delete", methods=["POST"])
def delete_scoring_sys(scoring_sys_id):
    if g.user:
        scoring_sys = Scoring_System.query\
            .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()

        associated_habits = User_Habit.query\
            .filter(User_Habit.scoring_system_id == scoring_sys.id).all()

        associated_goals = User_Goal.query\
            .filter(User_Goal.scoring_system_id == scoring_sys.id).all()


        if scoring_sys and not associated_habits and not associated_goals:

            db.session.delete(scoring_sys)

            try:
                db.session.commit()
            except Exception as e:
                flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
                print(e)
                db.session.rollback()
        else:
            flash("We were unable to delete this scoring system, please ensure you have appropriate access and there are not habits or goals linked to this system.", "warning")

        return redirect(url_for("tracking_bp.get_tracking_home"))
    else:
        flash("Please login to continue.", "warning")
        return redirect(url_for("home_bp.homepage"))  



###################################
# CRUD - Scoring System Parameters
###################################

# Read Scoring System Parameters
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params", methods=["GET"])
def get_new_scoring_params(scoring_sys_id):
    if g.user:

        scoring_system = Scoring_System.query.filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()

        parameters = Scoring_System.query\
                .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
                .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en,  Scoring_System_Params.id)\
                .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id))\
                .order_by(Scoring_System_Params.score_bp)\
                .all()

        form = ScoringSystemParamForm(request.form)

        return render_template("scoring_system_params.html", form = form, scoring_system = scoring_system, parameters = parameters)

    else:
        flash("You must be logged in to access that page.", "warning")
        return redirect(url_for("home_bp.homepage"))

# Create New Scoring System Parameter
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/new", methods=["POST"])
def add_new_scoring_param(scoring_sys_id):
    if g.user:
        form = ScoringSystemParamForm(request.form)

        scoring_system = Scoring_System.query.filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys_id)).first()

        parameters = Scoring_System_Params.query.filter(Scoring_System_Params.scoring_system_id == scoring_sys_id)

        breakpoints = [param.score_bp for param in parameters]

        if breakpoints:
            score_bp = max(breakpoints) + 1
        else:
            score_bp = 1

        if form.validate_on_submit():
            param = Scoring_System_Params(
                scoring_system_id = scoring_sys_id,
                score_bp = score_bp,
                score_input = form.score_input.data,
                score_output = form.score_output.data,
                name_en = form.name_en.data
            )

            # Try adding scoring system to database
            try:
                db.session.add(param)
                db.session.commit()    
            except Exception as e:
                flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
                print(e)
                db.session.rollback()

            return redirect(url_for("tracking_bp.get_new_scoring_params", scoring_sys_id = scoring_sys_id))

        else:
            return render_template("scoring_system_params.html", form = form, scoring_system = scoring_system, parameters = parameters)

# TODO
# Update Scoring System Parameter
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/<int:scoring_param_id>/edit", methods=["GET"])
def get_edit_scoring_param(scoring_sys_id, scoring_param_id):
    return redirect(url_for("tracking_bp.add_new_scoring_param"))

@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/<int:scoring_param_id>/edit", methods=["POST"])
def update_scoring_param(scoring_sys_id, scoring_param_id):
    return redirect(url_for("tracking_bp.add_new_scoring_param"))

# Delete Scoring System Parameter
@tracking_bp.route("/scoring_sys/<int:scoring_sys_id>/params/<int:scoring_param_id>/delete", methods=["POST"])
def delete_scoring_param(scoring_sys_id, scoring_param_id):
    return redirect(url_for("tracking_bp.add_new_scoring_param"))


###################################
# CRUD - Goal Scores
###################################
# TODO
# View All Goal Scores
@tracking_bp.route("/goal_scores/<int:goal_id>", methods=["GET"])
def get_goal_scores(goal_id):
    return redirect(url_for("tracking_bp.get_new_goal_score"))

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
        
        form.date.data = datetime.today()

        return render_template("goal_score_new.html", form = form, user_goal = user_goal)

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

# TODO
# Update Goal Score
@tracking_bp.route("/goal_scores/<int:goal_id>/scores/<int:score_id>/update", methods=["GET"])
def get_edit_goal_score(goal_id):
    return redirect(url_for("tracking_bp.get_new_goal_score"))

@tracking_bp.route("/goal_scores/<int:goal_id>/scores/<int:score_id>/update", methods=["POST"])
def update_goal_score(goal_id):
    return redirect(url_for("tracking_bp.get_new_goal_score"))

# Delete Goal Score
@tracking_bp.route("/goal_scores/<int:goal_id>/scores/<int:score_id>/delete", methods=["POST"])
def delete_goal_score(goal_id):
    return redirect(url_for("tracking_bp.get_new_goal_score"))


###################################
# CRUD - Habit Scores
###################################
# TODO
# View All Habit Scores
@tracking_bp.route("/habit_scores/<int:habit_id>", methods=["GET"])
def get_habit_scores(habit_id):
    return redirect(url_for("tracking_bp.get_new_habit_score"))

@tracking_bp.route("/habit_scores/<habit_id>/new", methods=["GET"])
def get_new_habit_score(habit_id):
    if g.user:
        form = HabitScoreForm()

        user_habit = User_Habit.query\
            .join(Habit, Habit.id == User_Habit.habit_id)\
            .add_columns(Habit.title_en, Habit.description_public)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id))\
            .first()
        
        form.date.data = datetime.today()

        return render_template("habit_score_new.html", form = form, user_habit = user_habit)

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

# TODO
# Update Habit Score
@tracking_bp.route("/habit_scores/<int:habit_id>/scores/<int:score_id>/update", methods=["GET"])
def get_edit_habit_score(habit_id):
    return redirect(url_for("tracking_bp.get_new_habit_score"))

@tracking_bp.route("/habit_scores/<int:habit_id>/scores/<int:score_id>/update", methods=["POST"])
def update_habit_score(habit_id):
    return redirect(url_for("tracking_bp.get_new_habit_score"))

# Delete Habit Score
@tracking_bp.route("/habit_scores/<int:habit_id>/scores/<int:score_id>/delete", methods=["POST"])
def delete_habit_score(habit_id):
    return redirect(url_for("tracking_bp.get_new_habit_score"))




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
        

        filter_after = datetime.today() - timedelta(days = qty_days)

        # filter_after = datetime(2020, 8, 3, 13, 39, 13, 288470) - timedelta(days = qty_days)

        score_results = User_Habit.query\
            .join(Habit_Score, User_Habit.id == Habit_Score.habit_id)\
            .add_columns(Habit_Score.date, Habit_Score.score)\
            .filter(and_(User_Habit.user_id == g.user.id, User_Habit.id == habit_id, Habit_Score.date >= filter_after))\
            .order_by(Habit_Score.date)\
            .all()

        if score_results:
            scoring_sys = score_results[0].User_Habit.scoring_system_id

            system_parameters = Scoring_System.query\
                    .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
                    .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en)\
                    .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys))\
                    .order_by(Scoring_System_Params.score_bp)\
                    .all()


            description = {
                "date":   ("datetime", "Time Spent"),
                "score": ("number", "Score"),
                "score_label":  ("string",'',{'role':'tooltip'})
                }

            data = []

            len_param_list = len(system_parameters)

            for result in score_results:
                data_point = {
                    "date": result.date,
                    "score": None,
                    "score_label": None
                }

                for idx, param in enumerate(system_parameters):
                    if result.score <= system_parameters[idx].score_input:
                        data_point["score"] = param.score_output
                        data_point["score_label"] = param.name_en
                        break
                    elif result.score > system_parameters[idx].score_input and idx == (len_param_list - 1):
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

            # print(jsonResponse)

        else:
            jsonResponse = {'info': 'No data available.'}

        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse

@tracking_bp.route("/user_goal_scores")
def get_user_goal_scores():
    if g.user:

        goal_id = request.args.get('goal_id')
        qty_days = int(request.args.get('qty_days'))
        

        filter_after = datetime.today() - timedelta(days = qty_days)

        # filter_after = datetime(2020, 8, 3, 13, 39, 13, 288470) - timedelta(days = qty_days)

        score_results = User_Goal.query\
            .join(Goal_Score, User_Goal.id == Goal_Score.goal_id)\
            .add_columns(Goal_Score.date, Goal_Score.score)\
            .filter(and_(User_Goal.user_id == g.user.id, User_Goal.id == goal_id, Goal_Score.date >= filter_after))\
            .order_by(Goal_Score.date)\
            .all()

        if score_results:
            scoring_sys = score_results[0].User_Goal.scoring_system_id

            system_parameters = Scoring_System.query\
                    .join(Scoring_System_Params, Scoring_System.id == Scoring_System_Params.scoring_system_id)\
                    .add_columns(Scoring_System_Params.score_bp, Scoring_System_Params.score_input, Scoring_System_Params.score_output, Scoring_System_Params.name_en)\
                    .filter(and_(Scoring_System.user_id == g.user.id, Scoring_System.id == scoring_sys))\
                    .order_by(Scoring_System_Params.score_bp)\
                    .all()


            description = {
                "date":   ("datetime", "Time Spent"),
                "score": ("number", "Score"),
                "score_label":  ("string",'',{'role':'tooltip'})
                }

            data = []

            len_param_list = len(system_parameters)

            for result in score_results:
                data_point = {
                    "date": result.date,
                    "score": None,
                    "score_label": None
                }

                for idx, param in enumerate(system_parameters):
                    if result.score <= system_parameters[idx].score_input:
                        data_point["score"] = param.score_output
                        data_point["score_label"] = param.name_en
                        break
                    elif result.score > system_parameters[idx].score_input and idx == (len_param_list - 1):
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

            # print(jsonResponse)

        else:
            jsonResponse = {'info': 'No data available.'}

        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse



