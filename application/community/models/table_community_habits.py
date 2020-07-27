from application import db

Community_Habits = db.Table("community_habits", 
    db.Column(  'habit_id',
                db.Integer,
                db.ForeignKey('habit.id'),
                primary_key = True),
    db.Column(  'community_id',
                db.Integer,
                db.ForeignKey('community.id'), 
                primary_key = True))

