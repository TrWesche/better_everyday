from flask import Blueprint, render_template
from flask import current_app as app
import requests
from ..services.api_pexels.api_core_photos import get_photo

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route("/")
def homepage():
    image_resp = get_photo(708440)

    if image_resp.status_code != 200:
        image_url = "application\DB_Schema.png"
    else:
        image_dict = image_resp.json()
        image_list = image_dict.get("src")
        print(image_list)
        image_url = image_list.get("landscape")
        print(image_url)

    return render_template('home.html', image_url = image_url)