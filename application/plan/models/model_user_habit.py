from application import db

class User_Habit(db.Model):

    __tablename__ = "user_habit"

    id = db.Column(db.Integer, primary_key = True)

    active = db.Column(db.Boolean, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'))

    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable = False)

    scoring_system_id = db.Column(db.Integer, db.ForeignKey('scoring_system.id'))
    
    schedule_id = db.Column(db.Integer, db.ForeignKey('reminder_schedule.id'))

