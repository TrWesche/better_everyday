from application import db

class Reminder_Schedule(db.Model):

    __tablename__ = "reminder_schedule"

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    title_en = db.Column(db.String(50), nullable = False)

    description = db.Column(db.String(500))

    public = db.Column(db.Boolean, nullable = False, default=False)

    global_time = db.Column(db.DateTime(timezone=True))

    monday = db.Column(db.Boolean, nullable = False)

    monday_time = db.Column(db.DateTime(timezone=True))

    tuesday = db.Column(db.Boolean, nullable = False)

    tuesday_time = db.Column(db.DateTime(timezone=True))

    wednesday = db.Column(db.Boolean, nullable = False)

    wednesday_time = db.Column(db.DateTime(timezone=True))

    thursday = db.Column(db.Boolean, nullable = False)

    thursday_time = db.Column(db.DateTime(timezone=True))

    friday = db.Column(db.Boolean, nullable = False)

    friday_time = db.Column(db.DateTime(timezone=True))

    saturday = db.Column(db.Boolean, nullable = False)

    saturday_time = db.Column(db.DateTime(timezone=True))

    sunday = db.Column(db.Boolean, nullable = False)

    sunday_time = db.Column(db.DateTime(timezone=True))