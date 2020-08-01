from flask_bcrypt import Bcrypt
from application import db

bcrypt = Bcrypt()

class Authentication(db.Model):

    __tablename__ = "authentication"

    username = db.Column(db.String(50),
                primary_key = True)

    password = db.Column(db.String,
                nullable = False)

    # OPTION: Add additional column to store password salt

    @classmethod
    def register(cls, username, password):
        print(password)

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        u = cls.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False
