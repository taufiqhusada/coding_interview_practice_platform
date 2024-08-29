
from flask import Flask, send_file, request
from flask_socketio import SocketIO, send, disconnect
import openai
import time
import os


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
socketio = SocketIO(app)


client = init_openai_config()

start_time = time.time()

def call_open_api(message):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a Hiring Manager that conduct a software engineering interview"},
            {'role': 'user', 'content': message}
        ],
        temperature=0,
        stream=True
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

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    manager.connect(sid)
    print(f"Client {sid} connected")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    manager.disconnect(sid)
    print(f"Client {sid} disconnected")

@socketio.on('message')
def handle_message(data):
    sid = request.sid
    print(f"Received text: {data}")
    
    try:
        res = call_open_api(data)
        collected_chunks = []
        collected_messages = []
        
        for chunk in res:
            chunk_time = time.time() - start_time
            collected_chunks.append(chunk)
            chunk_message = chunk.choices[0].delta.content
            collected_messages.append(chunk_message)
            
            if chunk_message and '.' in chunk_message:
                message = ''.join([m for m in collected_messages if m])
                manager.send_text(message, sid)
                collected_messages = []
            
            print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")

        if collected_messages:
            message = ''.join([m for m in collected_messages if m])
            manager.send_text(message, sid)
            collected_messages = []

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


