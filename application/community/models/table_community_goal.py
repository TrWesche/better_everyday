from application import db

Community_Goal = db.Table("community_goal", 
    db.Column(  'goal_id',
                db.Integer,
                db.ForeignKey('goal.id'),
                primary_key = True),
    db.Column(  'community_id',
                db.Integer,
                db.ForeignKey('community.id'), 
                primary_key = True))

