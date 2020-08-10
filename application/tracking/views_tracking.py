from flask import Blueprint, render_template, redirect, flash, request, session, g, jsonify
from flask import current_app as app
from sqlalchemy import exc, and_
from .models.model_habit_score import Habit_Score
from .models.model_goal_score import Goal_Score
from .models.model_scoring_system import Scoring_System
from .models.model_scoring_system_params import Scoring_System_Params
from .models.model_reminder_schedule import Reminder_Schedule
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
    return render_template("tracking_home.html")


# @tracking_bp.route("/api/dt_scoring_sys", methods=["GET"])
# def get_dt_scoring_sys():

#     scoring_system_description = {
#         "time_input":   ("number", "Time Spent"),
#         "score_output": ("number", "Score"),
#         "score_label":  ("string",'',{'role':'tooltip'})
#         }

#     scoring_system_data = [{"time_input": 0, "score_output": 0, "score_label": ""},
#         {"time_input": 59, "score_output": 0, "score_label": "F"},
#         {"time_input": 69, "score_output": 1, "score_label": "D"},
#         {"time_input": 79, "score_output": 2, "score_label": "C"},
#         {"time_input": 89, "score_output": 3, "score_label": "B"},
#         {"time_input": 100, "score_output": 4, "score_label": "A"}
#     ]


    
#     data_table = gviz_api.DataTable(scoring_system_description)
#     data_table.LoadData(scoring_system_data)

#     jsonResponse = data_table.ToJSonResponse(columns_order=("time_input", "score_output", "score_label"),
#                                 order_by="time_input")

#     return jsonResponse


@tracking_bp.route("/scoring_sys")
def get_scoring_sys():
    if g.user:

        print("Hit")

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