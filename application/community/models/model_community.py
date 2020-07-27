from application import db

class Community(db.Model):

    __tablename__ = "community"

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(50), nullable = False)

    description = db.Column(db.String(500), nullable = False)

    personas = db.relationship('Community_Personas', backref='communities', cascade="all, delete-orphan")

    habits = db.relationship('Community_Habits', backref='communities', cascade="all, delete-orphan")