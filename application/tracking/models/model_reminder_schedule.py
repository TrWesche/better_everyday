from application import db

class Reminder_Schedule(db.Model):

    __tablename__ = "reminder_schedule"

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(50), nullable = False)

    description = db.Column(db.String(500))

    public = db.Column(db.Boolean, nullable = False)

    global_time = db.Column(db.DateTime)

    monday = db.Column(db.Boolean, nullable = False)

    monday_time = db.Column(db.DateTime)

    tuesday = db.Column(db.Boolean, nullable = False)

    tuesday_time = db.Column(db.DateTime)

    wednesday = db.Column(db.Boolean, nullable = False)

    wednesday_time = db.Column(db.DateTime)

    thursday = db.Column(db.Boolean, nullable = False)

    thursday_time = db.Column(db.DateTime)

    friday = db.Column(db.Boolean, nullable = False)

    friday_time = db.Column(db.DateTime)

    saturday = db.Column(db.Boolean, nullable = False)

    saturday_time = db.Column(db.DateTime)

    sunday = db.Column(db.Boolean, nullable = False)

    sunday_time = db.Column(db.DateTime)