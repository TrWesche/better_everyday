from application import db

class Goal_Score(db.Model):

    __tablename__ = "goal_score"

    id = db.Column(db.Integer, primary_key = True)

    date = db.Column(db.DateTime(timezone=True), nullable = False)

    score = db.Column(db.Float, nullable = False)

    goal_id = db.Column(db.Integer, db.ForeignKey('user_goal.id'))