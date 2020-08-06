from application import db

class Scoring_System(db.Model):

    __tablename__ = "scoring_system"

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    title_en = db.Column(db.String(50), nullable = False)

    description = db.Column(db.String(500))

    public = db.Column(db.Boolean, nullable = False)

    params = db.relationship('Scoring_System_Params', backref='scoring_system', cascade="all, delete-orphan")