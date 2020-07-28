from application import db

class Habit_Score(db.Model):

    __tablename__ = "habit_score"

    id = db.Column(db.Integer, primary_key = True)

    date = db.Column(db.DateTime, nullable = False)

    score = db.Column(db.Float, nullable = False)

    habit_id = db.Column(db.Integer, db.ForeignKey('user_habit.id'))