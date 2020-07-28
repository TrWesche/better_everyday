from flask import Blueprint, render_template, redirect, flash, request, session
from flask import current_app as app
from sqlalchemy import exc
from .models.model_user import User
from application import db


# Blueprint Configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@user_bp.route("/users", methods=["GET"])
def get_user_list():
    return render_template("user_list.html")

@user_bp.route("/users/<user_id>", methods=["POST"])
def create_user_profile(user_id):
    return redirect("user_profile.html")


@user_bp.route("/users/<user_id>", methods=["GET"])
def get_user_profile(user_id):
    return render_template("user_profile.html")


@user_bp.route("/users/<user_id>", methods=["PUT"])
def update_user_profile(user_id):
    return redirect("user_profile.html")


@user_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user_profile(user_id):
    return redirect("/")