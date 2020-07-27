from flask import Blueprint, render_template, redirect, flash, request, session
from flask import current_app as app
from sqlalchemy import exc
from models.model_auth import Authentication
from application import db


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route("/register", methods=["GET"])
def get_registration_from():
    return render_template("user_registration.html")

@auth_bp.route("/register", methods=["POST"])
def create_user_auth():
    return redirect("home.html")

@auth_bp.route("/login", methods=["GET"])
def get_login_form():
    return render_template("user_login.html")

@auth_bp.route("/login", methods=["POST"])
def process_user_login():
    return redirect("home.html")
