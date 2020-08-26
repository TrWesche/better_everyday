from flask import Blueprint, render_template, redirect, flash, request, session, g, url_for
from flask import current_app as app
from sqlalchemy import exc
from sqlalchemy.orm import load_only
from .models.model_user import User
from .forms.form_user_update import UserUpdateFrom

from application import db

# Blueprint Configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@user_bp.route("/", methods=["GET"])
def get_user_list():
    if g.user:  
        args = request.args
        fields = ['username', 'first_name']

        if "username" in args:
            username = args.get("username")
            users = db.session.query(User).filter(User.username.like(f"%{username}%")).options(load_only(*fields)).all()
        else:
            users = db.session.query(User).options(load_only(*fields)).all()

        return render_template("user_all.html", user_list = users)

    flash("You must be logged in to access that page.", "warning")
    return redirect(url_for("home_bp.homepage"))


@user_bp.route("/<username>", methods=["GET"])
def get_user_profile(username):
    if g.user:

        user = User.query.get(g.user.id)

        if username == user.username:
            return render_template("user_profile_page.html", user = user)

    flash("You must be logged in to access that page.", "warning")
    return redirect(url_for("home_bp.homepage"))



@user_bp.route("/<username>/edit", methods=["GET"])
def get_update_user(username):
    if g.user:

        user = User.query.get(g.user.id)

        if username == user.username:
            form = UserUpdateFrom(
                first_name = user.first_name,
                last_name = user.last_name,
                email = user.email
            )

            return render_template("user_edit_page.html", form = form, user = user)


    flash("You must be logged in to access that page.", "warning")
    return redirect(url_for("home_bp.homepage"))


@user_bp.route("/<username>", methods=["POST"])
def update_user(username):
    if g.user:

        form = UserUpdateFrom(request.form)
        user = User.query.get(g.user.id)

        if username == user.username and form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data

            try:
                db.session.commit()
                return redirect(url_for("user_bp.get_user_profile", username = user.username))
            except Exception as e:
                flash("Error: Unable to update user persona - update action failed", "danger")
                print(e)
                db.session.rollback()  
            
        else:
            return render_template("user_edit_page.html", form = form, user = user)

    flash("You must be logged in to access that page.", "warning")
    return redirect(url_for("home_bp.homepage"))


# @user_bp.route("/<username>", methods=["DELETE"])
# def delete_user_profile(username):
#     return redirect("/")