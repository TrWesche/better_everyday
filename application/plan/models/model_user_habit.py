from application import db

class User_Habit(db.Model):

    __tablename__ = "user_habit"

    id = db.Column(db.Integer, primary_key = True)

    active = db.Column(db.Boolean, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    user_persona_id = db.Column(db.Integer, db.ForeignKey('user_persona.id'))

    scoring_system_id = db.Column(db.Integer, db.ForeignKey('scoring_system.id'))
    
    schedule_id = db.Column(db.Integer, db.ForeignKey('reminder_schedule.id'))

    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable = False)

    linked_goal_id = db.Column(db.Integer, db.ForeignKey('user_goal.id'))

    description_private = db.Column(db.String(500))

    # persona = db.relationship("Persona", secondary = "user_persona", primaryjoin=("User_Habit.user_persona_id == User_Persona.id"), secondaryjoin=("User_Persona.id == Persona.id"))

    habit = db.relationship("Habit", primaryjoin="and_(User_Habit.habit_id == Habit.id)")

    goal = db.relationship("User_Goal", primaryjoin=("and_(User_Habit.linked_goal_id == User_Goal.id)"))

    scores = db.relationship("Habit_Score", primaryjoin="Habit_Score.habit_id == User_Habit.id", cascade="all, delete")