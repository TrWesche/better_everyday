from flask import Blueprint, render_template, redirect, flash, request, session
from flask import current_app as app
from sqlalchemy import exc
from models.model_community import Community
from models.model_thread import Thread
from models.model_post import Post
from models.table_community_habits import Community_Habits
from models.table_community_personas import Community_Personas
from application import db


# Blueprint Configuration
community_bp = Blueprint(
    'community_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@community_bp.route("/communities", methods=["GET"])
# TODO: Implement search functionality
def get_communities_list():
    return render_template("communities_list.html")


@community_bp.route("/communities/new", methods=["GET"])
def get_new_community_form():
    return render_template("communities_form.html")


@community_bp.route("/communities/new", methods=["POST"])
def create_new_community():
    return redirect("/communities")


@community_bp.route("/communities/<int:community_id>", methods=["GET"])
def get_community_page(community_id):
    return render_template("community_main.html")

# TODO: Define other routes for community posts, additions, deletions, etc.
