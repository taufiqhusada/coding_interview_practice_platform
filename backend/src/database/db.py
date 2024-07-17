
from flask_mongoengine import MongoEngine
import os

db = MongoEngine()

def initialize_db(app):
    app.config["mongo_uri"] = os.getenv("MONGO_URI")

    app.config['MONGODB_SETTINGS'] = {
        'db': 'interview_tool_db',
        'host': app.config["mongo_uri"]
    }

    db = MongoEngine(app)