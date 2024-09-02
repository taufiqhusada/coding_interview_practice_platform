
from flask import Flask, send_file, request
from flask_socketio import SocketIO, send, disconnect
import openai
import time
import os
import base64


from flask import Flask, request
from flask_cors import CORS
import os

from routes.AgentsSimulation import agentsSimulationBP
from database.db import initialize_db
from dotenv import load_dotenv

from flask_socketio import SocketIO


import firebase_admin
from firebase_admin import credentials, storage
from config.openai_connector import init_openai_config

load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,  cors_allowed_origins="*")


client = init_openai_config()

start_time = time.time()

def generate_tts(text):
    # Send a request to the OpenAI TTS API to generate audio from text
    tts_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="opus"
    )

    return tts_response.content


def call_open_api(message):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a Hiring Manager that conduct a software engineering interview"},
            {'role': 'user', 'content': message}
        ],
        temperature=0,
    )

    return completion

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    def connect(self, sid):
        self.active_connections.append(sid)

    def disconnect(self, sid):
        self.active_connections.remove(sid)

    def send_text(self, text, sid):
        send(text, room=sid)

manager = ConnectionManager()

@socketio.on('connect', namespace='/ws')
def handle_connect():
    sid = request.sid
    manager.connect(sid)
    print(f"Client {sid} connected")

@socketio.on('disconnect', namespace='/ws')
def handle_disconnect():
    sid = request.sid
    manager.disconnect(sid)
    print(f"Client {sid} disconnected")

@socketio.on('message', namespace='/ws')
def handle_message(data):
    sid = request.sid
    print(f"Received text: {data}")
    
    try:
        res = call_open_api(data)
        message = res.choices[0].message.content

        audio = generate_tts(message)
        audio_base64 = base64.b64encode(audio).decode('utf-8')
        data = {'audio_data': audio_base64,'text_response': message}

        manager.send_text(data, sid)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        disconnect(sid)

initialize_db(app)
@app.route("/")
def hello_world():
    return  "hello world"

app.register_blueprint(agentsSimulationBP)


if __name__ == "__main__":

    socketio.run(app)


# cred = credentials.Certificate("firebase_config.json")
# firebase_admin.initialize_app(cred, {"storageBucket": os.getenv('FIREBASE_BUCKET')})


