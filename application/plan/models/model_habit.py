from application import db

class Habit(db.Model):

    __tablename__ = "habit"

    id = db.Column(db.Integer, primary_key = True)

    title_en = db.Column(db.String(50), nullable = False)

    description_public = db.Column(db.String(500), nullable = False)

    # Collation column is intended to collate multiple versions of the same "Habit" in the future for improved linking to communities
    collate = db.Column(db.Integer)
