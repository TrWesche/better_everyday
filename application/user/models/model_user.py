from application import db

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(50),
                nullable = False)

    last_name = db.Column(db.String(50),
                nullable = False)

    email = db.Column(db.String(100),
                nullable = False)

    username = db.relationship('Authentication', backref='user', cascade="all, delete-orphan")