from application import db

class Thread(db.Model):

    __tablename__ = "thread"

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(50), nullable = False)

    description = db.Column(db.String(500), nullable = False)

    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

    posts = db.relationship('Post', backref='thread', cascade="all, delete-orphan")