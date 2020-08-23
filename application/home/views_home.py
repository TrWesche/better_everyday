from flask import Blueprint, render_template, g, url_for, redirect
from flask import current_app as app
# import requests

from sqlalchemy import and_

from datetime import datetime, timedelta, timezone

from ..services.api_pexels.api_core_photos import get_photo
from ..plan.models.model_user_persona import User_Persona
from ..plan.models.model_persona import Persona

from ..plan.models.model_user_habit import User_Habit
from ..plan.models.model_habit import Habit
from ..plan.models.model_user_goal import User_Goal
from ..plan.models.model_goal import Goal



# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home/static'
)

@home_bp.route("/")
def homepage():
    # Get Carousel Images
    carousel_image_list = []

    image_resp = get_photo(708440) # Group of friends
    if image_resp.status_code != 200:
        carousel_obj = {
            "landscape_image_url": "application\home\static\pexels-pixabay-36717.jpg",
            "carousel_text": "Welcome to Better Everyday"
        }
        carousel_image_list.append(carousel_obj)
    else:
        image_dict = image_resp.json()
        image_list = image_dict.get("src")
        carousel_obj = {
            "landscape_image_url": image_list.get("landscape"),
            "carousel_text": "Welcome to Better Everyday"
        }
        carousel_image_list.append(carousel_obj)

    image_resp = get_photo(374068) # Girl Painting
    if image_resp.status_code == 200:
        image_dict = image_resp.json()
        image_list = image_dict.get("src")
        carousel_obj = {
            "landscape_image_url": image_list.get("landscape"),
            "carousel_text": "What will you Create?"
        }
        carousel_image_list.append(carousel_obj)

    image_resp = get_photo(1425297) # Man Playing Guitar
    if image_resp.status_code == 200:
        image_dict = image_resp.json()
        image_list = image_dict.get("src")
        carousel_obj = {
            "landscape_image_url": image_list.get("landscape"),
            "carousel_text": "What will you perform?"
        }
        carousel_image_list.append(carousel_obj)

    image_resp = get_photo(4144144) # Boy Studying
    if image_resp.status_code == 200:
        image_dict = image_resp.json()
        image_list = image_dict.get("src")
        carousel_obj = {
            "landscape_image_url": image_list.get("landscape"),
            "carousel_text": "What will you learn?"
        }
        carousel_image_list.append(carousel_obj)

    carousel_obj = {
            "landscape_image_url": url_for('.static', filename = "pexels-pixabay-36717.jpg"),
            "carousel_text": "Let us help you achieve more"
        }
    carousel_image_list.append(carousel_obj)

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
                append_obj["id"] = persona.User_Persona.id
                append_obj["persona_id"] = persona.User_Persona.persona_id
                append_obj["persona_title"] = persona.title_en
                append_obj["description_private"] = persona.User_Persona.description_private
                append_obj["description_public"] = persona.description_public
                append_obj["linked_habits"] = []
                append_obj["linked_goals"] = []

                for habit in user_habits:
                    if habit.User_Habit.user_persona_id == persona.User_Persona.id:
                        habit_obj = {}
                        habit_obj["id"] = habit.User_Habit.id
                        habit_obj["title"] = habit.title_en
                        append_obj.get("linked_habits").append(habit_obj)

                for goal in user_goals:
                    if goal.User_Goal.user_persona_id == persona.User_Persona.id:
                        goal_obj = {}
                        goal_obj["id"] = goal.User_Goal.id
                        goal_obj["title"] = goal.title_en
                        append_obj.get("linked_goals").append(goal_obj)

                persona_render_list.append(append_obj)


        return render_template('home.html', carousel_image_list = carousel_image_list, user_personas = user_personas, persona_render_list = persona_render_list)

    return render_template('home.html', carousel_image_list = carousel_image_list)