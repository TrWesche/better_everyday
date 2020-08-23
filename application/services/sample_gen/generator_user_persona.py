from application.plan.models.model_persona import Persona
from application.plan.models.model_user_persona import User_Persona

from application import db

def checkPersona(title_en):
    persona_result = Persona.query.filter(Persona.title_en == title_en.lower()).first()

    if persona_result:
        return persona_result.id
    else:
        return 0


def generatePersona(title_en, description_public):
    new_persona = Persona(title_en = title_en.lower(), description_public = description_public)

    db.session.add(new_persona)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate persona")

    return new_persona.id


def generateUserPersona(title_en, description_public, user_id, description_private):
    persona_id = checkPersona(title_en)
    if not persona_id:
        persona_id = generatePersona(title_en, description_public)

    new_user_persona = User_Persona(
        active = True,
        user_id = user_id,
        persona_id = persona_id,
        description_private = description_private
    )

    db.session.add(new_user_persona)
    
    try:
        db.session.commit()
    except:
        print("Failed to generate user persona")

    return new_user_persona.id