from ..application.tracking.models.model_scoring_system import Scoring_System
from ..application.tracking.models.model_scoring_system_params import Scoring_System_Params

from ..application import db

def CreateScore(user_id, title_en, description, public):
    s = Scoring_System(
        user_id = user_id,
        title_en = title_en,
        description = description,
        public = public
    )

    db.session.add(s)
    db.session.commit()

    return s.id


def CreateScoreParam(scoring_system_id, score_bp, score_input, score_output, name_en):
    s = Scoring_System_Params(
        scoring_system_id = scoring_system_id,
        score_bp = score_bp,
        score_input = score_input, 
        score_output = score_output,
        name_en = name_en
    )

    db.session.add(s)
    db.session.commit()

    return