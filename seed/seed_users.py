from ..application.authentication.models.model_auth import Authentication
from ..application.user.models.model_user import User

from ..application import db

def CreateUser(username, password, first_name, last_name, email):
    a = Authentication(
        username = username,
        password = password
    )

    db.session.add(a)
    db.session.commit()
 
    u = User(
        first_name = first_name,
        last_name = last_name,
        email = email,
        username = username,
        public = True
    )

    db.session.add(u)
    db.session.commit()

    return (u.id)