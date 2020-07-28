from flask import Blueprint, render_template, redirect, flash, request, session
from flask import current_app as app
from sqlalchemy import exc
from .models.model_persona import Persona
from .models.model_habit import Habit
from .models.model_goal import Goal
from .models.table_user_persona import User_Persona
from .models.table_user_habit import User_Habit
from .models.table_user_goal import User_Goal
from application import db


# Blueprint Configuration
habit_bp = Blueprint(
    'habit_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


# TODO: Implement routes
@habit_bp.route("/habits", methods=["GET"])
def get_communities_list():
    return render_template("habits_list.html")
