from flask import Blueprint, render_template, redirect, flash, request, session, g
from flask import current_app as app
from sqlalchemy import exc
from sqlalchemy.orm import load_only
from .models.model_user import User
from application import db

# Blueprint Configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@user_bp.route("/", methods=["GET"])
def get_user_list():   
    args = request.args
    print(args)
    fields = ['username', 'first_name']

    if "username" in args:
        username = args.get("username")
        users = db.session.query(User).filter(User.username.like(f"%{username}%")).options(load_only(*fields)).all()
    else:
        users = db.session.query(User).options(load_only(*fields)).all()

    print(users)

    return render_template("user_all.html", user_list = users)


@user_bp.route("/<username>", methods=["GET"])
def get_user_profile(username):
    return render_template("user_profile.html")


@user_bp.route("/<username>", methods=["PATCH"])
def update_user_profile(username):
    return redirect("user_profile.html")


@user_bp.route("/<username>", methods=["DELETE"])
def delete_user_profile(username):
    return redirect("/")