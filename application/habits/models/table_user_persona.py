from application import db

User_Persona = db.Table("user_persona",
    db.Column(  'id',
                db.Integer,
                primary_key = True),
    db.Column(  'user_id',
                db.Integer,
                db.ForeignKey('user.id')),
    db.Column(  'persona_id',
                db.Integer,
                db.ForeignKey('persona.id')))