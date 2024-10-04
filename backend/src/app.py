
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
from routes.GenerateSimulation import generateSimulationBP
from routes.GetFeedback import getFeedbackBP

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
        model='gpt-4o-mini',
        messages=messages,
        temperature=0
    )

    res = completion.choices[0].message.content
    return res

# def check_reply(input_data):
#     chat_messages = input_data['messages']
#     consecutive_user_messages = []

#     # Iterate backward through chat_messages to find the last consecutive user messages
#     for i in range(len(chat_messages) - 1, -1, -1):
#         consecutive_user_messages.append({'role': chat_messages[i]['role'] , 'content':chat_messages[i]['content']})

#         if chat_messages[i]['role'] != 'interviewee':
#             break  # Stop if an assistant message is encountered

#     # Reverse the list to maintain the original order
#     consecutive_user_messages.reverse()

#     prompt = f"""
#         You are an AI interviewer conducting a technical interview. After the candidate speaks or pauses, decide whether to "Reply" or "Not Reply" based on the following criteria:

#         Reply if:
#         - The candidate say hi
#         - The candidate asks a direct question or seeks clarification.
#         - The candidate appears stuck, confused, or has reached an incorrect conclusion.
#         - The candidate completes a segment of their thought process, and it's appropriate to provide feedback or guidance.
      
#         Not Reply if:
#         - The candidate is actively thinking aloud and logically processing their thoughts.
#         - The candidate is working through a problem or formulating a solution without needing immediate feedback.
#         - The candidate pauses briefly to think or review their approach.
        
#         Output:
#         Based on the candidate's current message, output either "Reply" or "Not Reply".

#         candidate current message:
#         {consecutive_user_messages}
        
#         """
  
    
#     messages=[
#         {"role": "system","content": prompt}, 
#     ]

#     res = client.chat.completions.create(
#         model='gpt-3.5-turbo',
#         messages=messages,
#         temperature=0
#     )

#     res = res.choices[0].message.content

#     print(messages, res)

#     return True if res == 'Reply' else False



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
                        You are an experienced technical interviewer conducting a coding interview. Your goal is to assess the candidate's problem-solving skills, coding ability, and communication. 
                            Make sure your communication is short and concise.
                        
                            The coding problem is the following:

                            Problem:
                            ```{problem}```

                            The candidate will implicitly follow these six steps:
                            1. Understanding: The candidate may ask clarifying questions to ensure they fully understand the problem and may propose an initial test case to demonstrate their understanding of the requirements.
                            2. Initial Ideation: The candidate will brainstorm initial ideas on how to solve the problem.
                            3. Idea Justification: The candidate will justify their approach, explaining why the chosen solution is suitable.
                            4. Implementation: The candidate will code the solution while thinking aloud to describe their thought process.
                            5. Review (Dry Run): After coding, the candidate will dry-run their code with a test case, walking through the logic step by step.
                            6. Evaluation: The candidate will evaluate their solution, discussing possible optimizations, edge cases, and any necessary improvements.

                            Throughout the interview:
                            - Prompt the candidate to think aloud and explain their reasoning at each step.
                            - Ask follow-up questions to gauge their understanding and depth of knowledge.
                            - If the candidate struggles, offer hints or guidance after they’ve made a reasonable attempt.
                            - Observe the correctness, efficiency, and clarity of their code and communication.
                            - Ignore the typo or grammar error from candidate answer
                            
                            At any point, you can refer to the candidate’s current code:

                            Candidate's Current Code:
                            ```{code}```

                            Make sure your communication is short and concise.
                        """},
        ]

    chat_messages = [{'content': item['content'], "role": 'user' if item['role'] == 'interviewee' else 'assistant'} for item in input_data['messages']]

    messages += chat_messages

    print(messages)
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages
    )

    return completion, chat_messages

def get_phase_interview(chat_messages):
    prompt = f"""Given the following interview transcript, classify which of the six steps the candidate is currently in based on the last part of the transcript. Consider both the interviewer's questions and the candidate's responses to determine the step:

            Transcript: 
            \"\"\"
            {chat_messages}
            \"\"\"


            mathematica
            Copy code
            <Insert transcript here>
            The candidate implicitly follows these six steps in a coding interview:

            - Understanding: The candidate responds to clarifying questions or asks their own to confirm understanding of the problem. The interviewer might prompt them for clarification or deeper understanding.
            - Initial Ideation: The candidate starts brainstorming solutions. The interviewer may encourage ideation or ask about possible approaches.
            - Idea Justification: The candidate explains why a particular solution is suitable. The interviewer might ask the candidate to defend or elaborate on their reasoning.
            - Implementation: The candidate begins coding while explaining their thought process. The interviewer might ask about specific lines of code or the rationale for implementation choices.
            - Review (Dry Run): The candidate tests their code with sample input and walks through the logic step by step. The interviewer may ask them to explain how they are validating the code.
            - Evaluation: The candidate evaluates the overall solution, discussing optimizations, edge cases, or improvements. The interviewer may prompt the candidate to think critically about their solution's performance or scalability.
            Classify the current step as one of the above. Your output should only be the step name (e.g., "Understanding"), without including the number.

            Classification: """
    
    res = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{
        "role": "system",
        "content": prompt
        }]
    )
    print(res)

    return res.choices[0].message.content

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections = []

#     def connect(self, sid):
#         self.active_connections.append(sid)

#     def disconnect(self, sid):
#         self.active_connections.remove(sid)

#     def send_text(self, text, sid):
#         send(text, room=sid)

# manager = ConnectionManager()

# @socketio.on('connect', namespace='/ws')
# def handle_connect():
#     sid = request.sid
#     manager.connect(sid)
#     print(f"Client {sid} connected")

# @socketio.on('disconnect', namespace='/ws')
# def handle_disconnect():
#     sid = request.sid
#     manager.disconnect(sid)
#     print(f"Client {sid} disconnected")


@app.route('/message', methods=['POST'])
def handle_message():
    try:
        data = request.json
        # sid = request.remote_addr  # or use any session/user identification mechanism
        print(f"Received text: {data}")

        if data['is_first'] == True:
            message = first_interaction()
            audio = generate_tts(message)
            audio_base64 = base64.b64encode(audio).decode('utf-8')
            response_data = {'audio_data': audio_base64, 'text_response': message, 'phase': 'Understanding'}

        else:
            res, transcript = call_open_api(data)
            message = res.choices[0].message.content
            transcript.append({'content': message, "role": 'assistant'})

            phase = get_phase_interview(transcript)

            audio = generate_tts(message)
            audio_base64 = base64.b64encode(audio).decode('utf-8')
            response_data = {'audio_data': audio_base64, 'text_response': message, 'phase': phase}

        # Return the response as JSON
        return response_data

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'error': str(e)}
    
initialize_db(app)
@app.route("/")
def hello_world():
    return  "hello world"

app.register_blueprint(agentsSimulationBP)
app.register_blueprint(generateSimulationBP)
app.register_blueprint(getFeedbackBP)


if __name__ == "__main__":

    socketio.run(app)


# cred = credentials.Certificate("firebase_config.json")
# firebase_admin.initialize_app(cred, {"storageBucket": os.getenv('FIREBASE_BUCKET')})


