from application import db

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(50),
                nullable = False)

    last_name = db.Column(db.String(50),
                nullable = False)

    email = db.Column(db.String(100),
                nullable = False)

    username = db.Column(db.String(50), db.ForeignKey('authentication.username'), unique=True)

    public = db.Column(db.Boolean, default=False)

    # auth = db.relationship('Authentication', backref='user', cascade="all, delete-orphan")

    personas = db.relationship(
                "User",
                secondary="user_persona",
                backref="persona_users")

    habits = db.relationship(
                "User",
                secondary="user_habit",
                backref="habit_users")
    
    goals = db.relationship(
                "User",
                secondary="user_goal",
                backref="goal_users"
    )

    @classmethod
    def register(cls, first_name, last_name, email, username):
        return cls(first_name = first_name, last_name = last_name, email=email, username = username)