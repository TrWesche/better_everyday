from application import db

class Goal(db.Model):

    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(50), nullable = False)

    description = db.Column(db.String(500), nullable = False)

    # Collation column is intended to collate multiple versions of the same "Goal" in the future for improved linking to communities
    collation = db.Column(db.Integer)
