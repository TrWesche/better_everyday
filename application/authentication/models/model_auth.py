from flask_bcrypt import Bcrypt
from application import db

bcrypt = Bcrypt()

class Authentication(db.Model):

    __tablename__ = "authentication"

    username = db.Column(db.String(50),
                primary_key = True)

    password = db.Column(db.String,
                nullable = False)

    # TODO: Register needs to create an entry in the User table in addition to the authentication table

    @classmethod
    def register(cls, username, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)

    # CODE BELOW IS FOR A SINGLE TABLE IMPLEMENTATION
    # def register(cls, username, password, email, first_name, last_name):
    #     hashed = bcrypt.generate_password_hash(password)
    #     hashed_utf8 = hashed.decode("utf8")

    #     return cls(username=username, password=hashed_utf8, email=email, 
    #                 first_name=first_name, last_name=last_name)


    @classmethod
    def authenticate(cls, username, password):
        u = cls.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False
