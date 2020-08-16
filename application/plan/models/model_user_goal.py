from application import db

class User_Goal(db.Model):

    __tablename__ = "user_goal"

    id = db.Column(db.Integer, primary_key = True)

    active = db.Column(db.Boolean, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    user_persona_id = db.Column(db.Integer, db.ForeignKey('user_persona.id'))

    scoring_system_id = db.Column(db.Integer, db.ForeignKey('scoring_system.id'))
    
    schedule_id = db.Column(db.Integer, db.ForeignKey('reminder_schedule.id'))

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = False)
    
    description_private = db.Column(db.String(500))

    # persona = db.relationship("Persona", secondary = "user_persona", primaryjoin=("User_Goal.user_persona_id == User_Persona.id"), secondaryjoin=("User_Persona.id == Persona.id"))

    goal = db.relationship("Goal", primaryjoin="and_(User_Goal.goal_id == Goal.id)")

    scores = db.relationship("Goal_Score", primaryjoin="Goal_Score.goal_id == User_Goal.id", cascade="all, delete")