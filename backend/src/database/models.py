"""
MongoDB Models - Only used when MongoDB is configured.
When MongoDB is not available, the StorageAdapter uses in-memory storage instead.
"""

from .db import db
import datetime


class InterviewTranscript(db.Document):
    sessionID = db.StringField(required=True, unique=True)
    datetime = db.DateTimeField(default=datetime.datetime.now)
    transcript = db.DynamicField()
    feedback = db.DynamicField()