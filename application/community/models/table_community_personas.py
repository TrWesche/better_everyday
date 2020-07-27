from application import db

Community_Personas = db.Table("community_personas", 
    db.Column(  'persona_id',
                db.Integer,
                db.ForeignKey('persona.id'),
                primary_key = True),
    db.Column(  'community_id',
                db.Integer,
                db.ForeignKey('community.id'), 
                primary_key = True))

