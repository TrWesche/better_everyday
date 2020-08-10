from application import db

class Goal(db.Model):

    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key = True)

    title_en = db.Column(db.String(50), nullable = False)

    description_public = db.Column(db.String(500), nullable = False, default = "No description provided.")

    collate = db.Column(db.Integer)
