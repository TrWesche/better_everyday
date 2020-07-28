from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# Globally accessible libraries
db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.TestConfig')
    debug = DebugToolbarExtension(app)

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from .home import views_home
        from .authentication import views_auth
        from .user import views_user
        from .community import views_community
        from .habits import views_habits
        from .tracking import views_tracking
        
        # Register Blueprints
        app.register_blueprint(views_home.home_bp)
        app.register_blueprint(views_auth.auth_bp)
        app.register_blueprint(views_user.user_bp)
        app.register_blueprint(views_community.community_bp)
        app.register_blueprint(views_habits.habit_bp)
        app.register_blueprint(views_tracking.tracking_bp)

        # db.create_all()

        return app