from flask import Blueprint, render_template, redirect, flash, request, session, g, url_for
from flask import current_app as app
from sqlalchemy import exc
from sqlalchemy.orm import load_only
import functools
from .models.model_user import User
from .forms.form_user_update import UserUpdateFrom

from application import db

# Blueprint Configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

msg_not_logged_in = "Please login to continue."
msg_not_authorized = "You are not authorized to view that resource."

def login_required(func):
    """Make sure user is logged in before proceeding"""
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if not g.user:
            flash(msg_not_logged_in, "warning")
            return redirect(url_for("home_bp.homepage"))
        return func(*args, **kwargs)
    return wrapper_login_required

@user_bp.route("/", methods=["GET"])
@login_required
def get_user_list():
    args = request.args
    fields = ['username', 'first_name']

    if "username" in args:
        username = args.get("username")
        users = db.session.query(User).filter(User.username.like(f"%{username}%")).options(load_only(*fields)).all()
    else:
        users = db.session.query(User).options(load_only(*fields)).all()

    return render_template("user_all.html", user_list = users)


@user_bp.route("/<username>", methods=["GET"])
@login_required
def get_user_profile(username):
    user = User.query.get(g.user.id)

    # If logged in user not the requested user, access not authorized
    if username != user.username:
        flash(msg_not_authorized, "danger")
        return redirect(url_for("home_bp.homepage"))
    
    return render_template("user_profile_page.html", user = user)    


@user_bp.route("/<username>/edit", methods=["GET"])
@login_required
def get_update_user(username):
    user = User.query.get(g.user.id)

    # If logged in user not the requested user, access not authorized
    if username != user.username:
        flash(msg_not_authorized, "danger")
        return redirect(url_for("home_bp.homepage"))

    form = UserUpdateFrom(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email
    )

    return render_template("user_edit_page.html", form = form, user = user)


@user_bp.route("/<username>", methods=["POST"])
@login_required
def update_user(username):
    form = UserUpdateFrom(request.form)
    user = User.query.get(g.user.id)

    # If logged in user not the requested user, access not authorized
    if username != user.username:
        flash(msg_not_authorized, "danger")
        return redirect(url_for("home_bp.homepage"))

    # If form data not valid, re-render page
    if not form.validate_on_submit():
        return render_template("user_edit_page.html", form = form, user = user)

    # Update user details and attempt update
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.email = form.email.data

    try:
        db.session.commit()
    except Exception as e:
        flash("Error: Unable to update user persona - update action failed", "danger")
        print(e)
        db.session.rollback()  

    return redirect(url_for("user_bp.get_user_profile", username = user.username))    



# @user_bp.route("/<username>", methods=["DELETE"])
# def delete_user_profile(username):
#     return redirect("/")