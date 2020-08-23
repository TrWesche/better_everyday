from application.tracking.models.model_scoring_system import Scoring_System
from application.tracking.models.model_scoring_system_params import Scoring_System_Params
from application import db

def generateScoringParams(scoring_system_id, param_list):
    session_param_list =[]

    for param in param_list:
        try:
            system_param = Scoring_System_Params(
                scoring_system_id = scoring_system_id,
                score_bp = param.get('score_bp'),
                score_input = param.get('score_input'),
                score_output = param.get('score_output'),
                name_en = param.get('name_en')
            )
        except Exception as e:
            print(e)
            print("Failed to add scoring system parameter")

        session_param_list.append(system_param)

    db.session.add_all(session_param_list)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        print("Failed to add scoring system parameters to db")


def generateScoringSystem(user_id, title_en, description, param_list):

    scoring_system = Scoring_System(
        user_id = user_id,
        title_en = title_en,
        description = description,
        public = False
    )

    db.session.add(scoring_system)

    try:
        db.session.commit()
    except:
        print("Failed to generate scoring system")

    generateScoringParams(scoring_system.id, param_list)

    return scoring_system.id