
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


def first_interaction():
    problem = """
    <b>Intersection of Two Arrays</b>
        <p>Given two integer arrays <code>nums1</code> and <code>nums2</code>, return an array of their intersection.</p>
        <p>Each element in the result must appear as many times as it shows in both arrays, and you may return the result in any order.</p>"""
    messages=[
            {"role": "system", 
             "content": f"""
                        You are a hiring manager conducting a coding interview. Your goal is to assess the candidate's problem-solving skills, coding ability, and communication. Begin by say hi and present the following coding problem:

                            Problem:
                            ```{problem}```
    
                        """},
        ]

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0
    )

    res = completion.choices[0].message.content
    return res

def check_reply(input_data):
    chat_messages = input_data['messages']
    consecutive_user_messages = []

    # Iterate backward through chat_messages to find the last consecutive user messages
    for i in range(len(chat_messages) - 1, -1, -1):
        consecutive_user_messages.append({'role': chat_messages[i]['role'] , 'content':chat_messages[i]['content']})

        if chat_messages[i]['role'] != 'interviewee':
            break  # Stop if an assistant message is encountered

    # Reverse the list to maintain the original order
    consecutive_user_messages.reverse()

    prompt = f"""
        You are an AI interviewer conducting a technical interview. After the candidate speaks or pauses, decide whether to "Reply" or "Not Reply" based on the following criteria:

        Reply if:
        - The candidate say hi
        - The candidate asks a direct question or seeks clarification.
        - The candidate appears stuck, confused, or has reached an incorrect conclusion.
        - The candidate completes a segment of their thought process, and it's appropriate to provide feedback or guidance.
        Not Reply if:

        - The candidate is actively thinking aloud and logically processing their thoughts.
        - The candidate is working through a problem or formulating a solution without needing immediate feedback.
        - The candidate pauses briefly to think or review their approach.
        
        Output:
        Based on the candidate's current message, output either "Reply" or "Not Reply".

        candidate current message:
        {consecutive_user_messages}
        
        """
  
    
    messages=[
        {"role": "system","content": prompt}, 
    ]

    res = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0
    )

    res = res.choices[0].message.content

    print(messages, res)

    return True if res == 'Reply' else False



def call_open_api(input_data):
    problem = """
    `<b>Intersection of Two Arrays</b>
        <p>Given two integer arrays <code>nums1</code> and <code>nums2</code>, return an array of their intersection.</p>
        <p>Each element in the result must appear as many times as it shows in both arrays, and you may return the result in any order.</p>

        <b>Example 1:</b>
        <pre><code>Input: nums1 = [1,2,2,1], nums2 = [2,2]\nOutput: [2,2]</code></pre>

        <b>Example 2:</b>
        <pre><code>Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]\nOutput: [4,9]</code></pre>
        <p>Note: [9,4] is also accepted.</p>`
    """

    code = input_data['code']

    messages=[
            {"role": "system", 
             "content": f"""
                        You are an experienced technical interviewer conducting a coding interview. Your goal is to assess the candidate's problem-solving skills, coding ability, and communication. The coding problem is the following:

                            Problem:
                            ```{problem}```

                            The candidate will implicitly follow these four steps:
                            1. Ask Clarifying Questions: The candidate will ask some clarifying questions to ensure they fully understand the problem.
                            2. Propose a Solution: Have the candidate outline their proposed solution, including the logic, data structures, and algorithms they plan to use.
                            3. Code the Solution: As they code, the candidate will explain their thought process, detailing how their code addresses the problem step by step.
                            4. Dry Run the Code: After coding, ask the candidate to simulate the execution of their code with a test case, explaining how each part of the code functions and what the expected output will be.

                            Throughout the interview:
                            - Prompt the candidate to think aloud and explain their reasoning at each step.
                            - Ask follow-up questions to gauge their understanding and depth of knowledge.
                            - If the candidate struggles, offer hints or guidance after they’ve made a reasonable attempt.
                            - Observe the correctness, efficiency, and clarity of their code and communication.
                            
                            At any point, you can refer to the candidate’s current code:

                            Candidate's Current Code:
                            ```{code}```
                        """},
        ]

    chat_messages = [{'content': item['content'], "role": 'user' if item['role'] == 'interviewee' else 'assistant'} for item in input_data['messages']]

    messages += chat_messages

    print(messages)
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
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
        if data['is_first'] == True:
            message = first_interaction()
            audio = generate_tts(message)
            audio_base64 = base64.b64encode(audio).decode('utf-8')
            data = {'audio_data': audio_base64,'text_response': message}

            manager.send_text(data, sid)

        elif check_reply(data):

            res = call_open_api(data)
            message = res.choices[0].message.content

            audio = generate_tts(message)
            audio_base64 = base64.b64encode(audio).decode('utf-8')
            data = {'audio_data': audio_base64,'text_response': message}

            manager.send_text(data, sid)
        else:
            data = {'audio_data': None,'text_response': None}
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


