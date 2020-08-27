from application.authentication.models.model_auth import Authentication
from application.user.models.model_user import User

from application import db

def generateAuthentication(username, password):
    new_auth = Authentication(username = username.lower(), 
        password = password)

    db.session.add(new_auth)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate authentication")

    return new_auth.username

def generateUser(username, first_name, last_name, email, public):
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        public = public
    )

    db.session.add(new_user)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate user")

    return new_user.id

def createUserAuth(username, password, first_name, last_name, email, public);
    auth_username = generateAuthentication(username, password)

    user_id = generateUser(auth_username.username, first_name, last_name, email, public)

    return user_id