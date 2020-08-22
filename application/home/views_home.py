from flask import Blueprint, render_template
from flask import current_app as app
import requests
from ..services.api_pexels.api_core_photos import get_photo

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home/static'
)

@home_bp.route("/")
def homepage():
    image_resp = get_photo(708440)

    if image_resp.status_code != 200:
        image_url = "application\DB_Schema.png"
    else:
        image_dict = image_resp.json()
        image_list = image_dict.get("src")
        image_url = image_list.get("landscape")

    return render_template('home.html', image_url = image_url)

# TODO:
# Upgrade homepage on user login to bring up dashboard with Persona area charts with data for
# each habit and goal which is linked to that certain persona as an individual layer of the chart.
# 
# Additionally under each chart will be a collapsable section where links for logging scores for each of
# the Persona's linked habits will be provided
#
# Additional metrics could be Total Time Spent on the Persona, Average Daily Activity, Average Activity per Day of the Week, etc.