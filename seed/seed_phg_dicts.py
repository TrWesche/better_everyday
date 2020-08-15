from ..application.plan.models.model_persona import Persona
from ..application.plan.models.model_habit import Habit
from ..application.plan.models.model_goal import Goal

from ..application import db

def CreatePersona(title_en, description_public):
    p = Persona(
        title_en = title_en,
        description_public = description_public
    )

    db.session.add(p)
    db.session.commit()

    return p.id


def CreateHabit(title_en, description_public):
    h = Habit(
        title_en = title_en,
        description_public = description_public
    )

    db.session.add(h)
    db.session.commit()

    return h.id


def CreateGoal(title_en, description_public):
    g = Goal(
        title_en = title_en,
        description_public = description_public
    )

    db.session.add(g)
    db.session.commit()

    return g.id