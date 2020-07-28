from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route("/")
def homepage():
    return render_template('home.html')