from flask import Blueprint, render_template, redirect, flash, request, session, url_for
from flask import current_app as app
from sqlalchemy import exc
from .models.model_community import Community
from .models.model_thread import Thread
from .models.model_post import Post
from .models.table_community_persona import Community_Persona
from .models.table_community_habit import Community_Habit
from .models.table_community_goal import Community_Goal
from application import db


# Blueprint Configuration
community_bp = Blueprint(
    'community_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@community_bp.route("/", methods=["GET"])
# TODO: Implement search functionality
def get_community_home():
    return render_template("community_home.html")


@community_bp.route("/new", methods=["GET", "POST"])
def get_new_community_form():
    return redirect(url_for("community_bp.get_communities_home"))


@community_bp.route("/<int:community_id>", methods=["GET"])
def get_community_page(community_id):
    return redirect(url_for("community_bp.get_communities_home"))

# TODO: Define other routes for community posts, additions, deletions, etc.
