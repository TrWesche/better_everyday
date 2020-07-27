from application import db

Habit_Goals = db.Table("habit_goals",
    db.Column(  'id',
                db.Integer,
                primary_key = True),
    db.Column(  'persona_habit_id',
                db.Integer,
                db.ForeignKey('persona_habits.id')),
    db.Column(  'goal_id',
                db.Integer,
                db.ForeignKey('goal.id')))