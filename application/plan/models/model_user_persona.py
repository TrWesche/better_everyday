from application import db

class User_Persona(db.Model):

    __tablename__ = "user_persona"

    id = db.Column(db.Integer, primary_key = True)

    active = db.Column(db.Boolean, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable = False)

    description_private = db.Column(db.String(500))

    persona = db.relationship("Persona", primaryjoin="and_(User_Persona.persona_id == Persona.id)")

    goals = db.relationship("User_Goal", primaryjoin="User_Goal.user_persona_id == User_Persona.id", cascade="all, delete")

    habits = db.relationship("User_Habit", primaryjoin="User_Habit.user_persona_id == User_Persona.id", cascade="all, delete")