from flask import Blueprint, render_template, redirect, flash, request, session, url_for, g
from flask import current_app as app
from sqlalchemy import exc

from .models.model_auth import Authentication
from ..user.models.model_user import User

from .forms.form_register import UserRegisterForm
from .forms.form_login import UserLoginForm

from application import db


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)



@auth_bp.before_app_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def do_login(user):
    """Log in user."""
    session["user_id"] = user.id


def do_logout():
    """Logout user."""
    session.clear()


@auth_bp.route("/register", methods=["GET", "POST"])
def user_registration():
    # TODO: Add sample data on account creation


    form = UserRegisterForm(request.form)

    login_user = False

    if form.validate_on_submit():
        auth = Authentication.register(
            username = form.username.data,
            password = form.password.data
        )

        user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )

        # Try adding data to authentication table
        try:
            db.session.add(auth)
            db.session.commit()
        except exc.IntegrityError:
            flash("Username already taken", "danger")
            db.session.rollback()
        except Exception as e:
            flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
            print(e)
            db.session.rollback()

        # Try adding data to user table
        try:
            db.session.add(user)
            db.session.commit() 
            login_user = True
        except Exception as e:
            flash("An error occured, if this problem persists please contact our user assistance dept", "danger")
            print(e)
            db.session.rollback()
            db.session.delete(auth)
            db.session.commit()

    if login_user:
        do_login(user)
        print("Error during add to session")
        return redirect(url_for('user_bp.get_user_list'))
    else:
        return render_template("user_register.html", form=form)



@auth_bp.route("/login", methods=["GET", "POST"])
def user_login():

    form = UserLoginForm(request.form)

    
    if form.validate_on_submit():
        # Authenticate login credentials
        auth = Authentication.authenticate(form.username.data,
                                            form.password.data)

        if auth:
            # If ok lookup user, should return only one value
            user = User.query.filter(User.username == auth.username).one()
            if user:
                do_login(user)
                flash(f"Welcome back {user.first_name}!", "success")
                return redirect(url_for("home_bp.homepage"))

        # If failure inform user
        flash("Incorrect username or password.", 'danger')

    # On get or login failure render login template
    return render_template('user_login.html', form=form)


@auth_bp.route("/logout", methods=["GET"])
def user_logout():

    do_logout()

    flash("See you next time!", "success")

    return redirect(url_for('home_bp.homepage'))


# TODO: User Profile Page

## TODO: Optional - Change Password Route