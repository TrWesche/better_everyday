from application import db

Community_Habit = db.Table("community_habit", 
    db.Column(  'habit_id',
                db.Integer,
                db.ForeignKey('habit.id'),
                primary_key = True),
    db.Column(  'community_id',
                db.Integer,
                db.ForeignKey('community.id'), 
                primary_key = True))

