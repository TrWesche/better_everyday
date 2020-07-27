from application import db

Persona_Habits = db.Table("persona_habits",
    db.Column(  'id',
                db.Integer,
                primary_key = True),
    db.Column(  'user_persona_id',
                db.Integer,
                db.ForeignKey('user_personas.id')),
    db.Column(  'habit_id',
                db.Integer,
                db.ForeignKey('habit.id')))