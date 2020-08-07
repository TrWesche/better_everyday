from application import db

class Scoring_System_Params(db.Model):

    __tablename__ = "scoring_system_params"

    id = db.Column(db.Integer, primary_key = True)

    scoring_system_id = db.Column(db.Integer, db.ForeignKey('scoring_system.id'))

    score_bp = db.Column(db.Integer, nullable = False)

    score_input = db.Column(db.Float, nullable = False)

    score_output = db.Column(db.Float, nullable = False)

    name_en = db.Column(db.String(50))