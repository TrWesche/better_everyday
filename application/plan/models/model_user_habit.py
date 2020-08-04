from application import db

class User_Habit(db.Model):

    __tablename__ = "user_habit"

    id = db.Column(db.Integer, primary_key = True)

    active = db.Column(db.Boolean, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    persona_id = db.Column(db.Integer, db.ForeignKey('user_persona.persona_id'))

    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable = False)

    scoring_system_id = db.Column(db.Integer, db.ForeignKey('scoring_system.id'))
    
    schedule_id = db.Column(db.Integer, db.ForeignKey('reminder_schedule.id'))

    persona = db.relationship("User_Persona", primaryjoin=("and_(User_Persona.persona_id == User_Habit.persona_id)"), backref='habits')

    habit = db.relationship("Habit", primaryjoin="and_(User_Habit.habit_id == Habit.id)")