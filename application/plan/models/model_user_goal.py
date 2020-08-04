from application import db

class User_Goal(db.Model):

    __tablename__ = "user_goal"

    id = db.Column(db.Integer, primary_key = True)

    active = db.Column(db.Boolean, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    persona_id = db.Column(db.Integer, db.ForeignKey('user_persona.persona_id'))

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = False)

    scoring_system_id = db.Column(db.Integer, db.ForeignKey('scoring_system.id'))
    
    schedule_id = db.Column(db.Integer, db.ForeignKey('reminder_schedule.id'))

    persona = db.relationship("User_Persona", primaryjoin=("and_(User_Persona.persona_id == User_Goal.persona_id)"), backref='goals')

    goal = db.relationship("Goal", primaryjoin="and_(User_Goal.goal_id == Goal.id)")