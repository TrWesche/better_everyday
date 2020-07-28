from flask import Blueprint, render_template, redirect, flash, request, session
from flask import current_app as app
from sqlalchemy import exc
from .models.model_habit_score import Habit_Score
from .models.model_goal_score import Goal_Score
from .models.model_scoring_system import Scoring_System
from .models.model_scoring_system_params import Scoring_System_Params
from .models.model_reminder_schedule import Reminder_Schedule
from application import db


# Blueprint Configuration
tracking_bp = Blueprint(
    'tracking_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


# TODO: Implement routes
@tracking_bp.route("/tracking", methods=["GET"])
def get_communities_list():
    return redirect("/")
