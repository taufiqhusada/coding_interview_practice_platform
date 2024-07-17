
from flask import Flask, request
from flask_cors import CORS
import os

from routes.AgentsSimulation import agentsSimulationBP
from database.db import initialize_db
from dotenv import load_dotenv


import firebase_admin
from firebase_admin import credentials, storage

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
initialize_db(app)

@app.route("/")
def hello_world():
    return  "hello world"

app.register_blueprint(agentsSimulationBP)

# cred = credentials.Certificate("firebase_config.json")
# firebase_admin.initialize_app(cred, {"storageBucket": os.getenv('FIREBASE_BUCKET')})


