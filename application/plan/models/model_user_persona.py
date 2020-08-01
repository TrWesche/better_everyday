from application import db

class User_Persona(db.Model):

    __tablename__ = "user_persona"

    id = db.Column(db.Integer, primary_key = True)

    active = db.Column(db.Boolean, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable = False)
