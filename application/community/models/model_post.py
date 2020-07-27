from application import db

class Post(db.Model):

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(50), nullable = False)

    content = db.Column(db.String, nullable = False)

    posted_time = db.Column(db.DateTime, nullable = False)

    edited_time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
