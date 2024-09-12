from .db import db
import datetime


class InterviewTranscript(db.Document):
    sessionID = db.StringField(required=True, unique=True)
    datetime = db.DateTimeField(default=datetime.datetime.now)
    transcript = db.DynamicField()