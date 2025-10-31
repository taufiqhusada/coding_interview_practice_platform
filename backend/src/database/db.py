
from flask_mongoengine import MongoEngine
import os

db = MongoEngine()

# Flag to track if MongoDB is enabled
USE_MONGODB = False

def initialize_db(app):
    global USE_MONGODB
    mongo_uri = os.getenv("MONGO_URI")
    
    if mongo_uri and mongo_uri.strip():
        # MongoDB is configured, use it
        app.config["mongo_uri"] = mongo_uri
        app.config['MONGODB_SETTINGS'] = {
            'DB': 'tech_interview',
            'host': mongo_uri
        }
        db.init_app(app)
        USE_MONGODB = True
        print("✓ MongoDB connected")
    else:
        # MongoDB not configured, use in-memory storage
        USE_MONGODB = False
        print("⚠ Running without MongoDB - using in-memory storage (data will be lost on restart)")