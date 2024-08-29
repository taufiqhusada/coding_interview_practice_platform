from flask import Blueprint, request
from flask_socketio import send, disconnect
import openai
import time

socketio_blueprint = Blueprint('socketio_blueprint', __name__)
start_time = time.time()

client = openai.OpenAI()

def call_open_api(message):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are an assistant named Bluu, a virtual assistant from ScalebuildAI, and you help people find the best product for them. Scalebuild is a software company."},
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

@socketio_blueprint.route('/ws')
def handle_connect():
    sid = request.sid
    manager.connect(sid)
    print(f"Client {sid} connected")

@socketio_blueprint.route('/ws')
def handle_disconnect():
    sid = request.sid
    manager.disconnect(sid)
    print(f"Client {sid} disconnected")

@socketio_blueprint.route('/ws')
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
