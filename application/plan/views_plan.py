from flask import Blueprint, render_template, redirect, flash, request, session
from flask import current_app as app
from sqlalchemy import exc
from .models.model_persona import Persona
from .models.model_habit import Habit
from .models.model_goal import Goal
from .models.model_user_persona import User_Persona
from .models.model_user_habit import User_Habit
from .models.model_user_goal import User_Goal
from application import db


# Blueprint Configuration
plan_bp = Blueprint(
    'plan_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


# TODO: Implement routes
@plan_bp.route("/plan", methods=["GET"])
def get_communities_list():
    return render_template("plan_home.html")
