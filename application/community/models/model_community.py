from application import db

class Community(db.Model):

    __tablename__ = "community"

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(50), nullable = False)

    description = db.Column(db.String(500), nullable = False)

    personas = db.relationship('Persona', secondary="community_persona", backref="communities")

    habits = db.relationship('Habit', secondary="community_habit", backref="communities")

    goals = db.relationship('Goal', secondary="community_goal", backref="communities")

    threads = db.relationship('Thread', backref='community', cascade="all, delete-orphan")

    # personas = db.relationship('Community_Personas', backref='communities', cascade="all, delete-orphan")

    # habits = db.relationship('Community_Habits', backref='communities', cascade="all, delete-orphan")

    # goals = db.relationship('Community_Goals', backref='communities', cascade="all, delete-orphan")