from flask import Blueprint, render_template, redirect, flash, request, session, g, jsonify
from flask import current_app as app
from sqlalchemy import exc, and_
from .models.model_habit_score import Habit_Score
from .models.model_goal_score import Goal_Score
from .models.model_scoring_system import Scoring_System
from .models.model_scoring_system_params import Scoring_System_Params
from .models.model_reminder_schedule import Reminder_Schedule

from ..plan.models.model_user_habit import User_Habit
from ..plan.models.model_user_goal import User_Goal

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

        for system in scoring_systems:
            print(system)

    else:
        flash("Please login to continue.", "warning")

    return render_template("tracking_home.html", scoring_systems = scoring_systems)



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
        

        # filter_after = datetime.today() - timedelta(days = qty_days)

        filter_after = datetime(2020, 8, 3, 13, 39, 13, 288470) - timedelta(days = qty_days)

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

            print(jsonResponse)

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
        

        # filter_after = datetime.today() - timedelta(days = qty_days)

        filter_after = datetime(2020, 8, 3, 13, 39, 13, 288470) - timedelta(days = qty_days)

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

            print(jsonResponse)

        else:
            jsonResponse = {'info': 'No data available.'}

        return jsonResponse

    else:
        jsonResponse = {'error': 'User must be authenticated to view that page.'}
        return jsonResponse