from flask import Blueprint, render_template, g, url_for, redirect
from flask import current_app as app
# import requests

from sqlalchemy import and_

from datetime import datetime, timedelta, timezone

from ..services.api_pexels.api_core_photos import get_photo
from ..plan.models.model_user_persona import User_Persona
from ..plan.models.model_persona import Persona



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
            .add_columns(Persona.title_en)\
            .filter(and_(User_Persona.user_id == g.user.id)).all()

        for persona in user_personas:
            print(persona)

        return render_template('home.html', carousel_image_list = carousel_image_list, user_personas = user_personas)


    return render_template('home.html', carousel_image_list = carousel_image_list)

# TODO:
# Upgrade homepage on user login to bring up dashboard with Persona area charts with data for
# each habit and goal which is linked to that certain persona as an individual layer of the chart.
# 
# Additionally under each chart will be a collapsable section where links for logging scores for each of
# the Persona's linked habits will be provided
#
# Additional metrics could be Total Time Spent on the Persona, Average Daily Activity, Average Activity per Day of the Week, etc.