
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
import os
import json
import base64

generateSimulationBP = Blueprint('generateSimulationBP', __name__)

@generateSimulationBP.route('/generateSimulation', methods=['POST'])
def generate_static_simulation():
    with open('routes/static/example_3_with_audio.json', 'r') as file:
        data = json.load(file)
        # data = generate_tts_from_generated_simulation(data)
    return data

# TODO: use this
def generate_simulation():
    data = request.json
    problem = data['problem']

    prompt = f"""
                Simulate a realistic coding interview between an interviewer and an interviewee focused on solving the given Problem. 
                The simulation should include explanations of best practices based on the example provided. When you write the code put it on "lines of code" and write and explain it step by step.
                Do not use built-in library if possible

                Format your answer into a json format:
                [{{"role(interviewer/ interviewee)": "", "content": "", "code (containing STEP BY STEP CODE that the interviewee write while think aloud)": "","explanation (when the role is interviewee, explain the importance or rationale of answering in a such way)": ""}}, ...]]

                The interviewer should ask probing questions to understand the interviewee's thought process, while the interviewee should clearly explain their approach, consider edge cases, and write code to solve the problem.

                The interviewer may offer hints if the interviewee gets stuck and should evaluate the solution's correctness, efficiency, and clarity. The interviewee should think aloud, asking clarifying questions if needed and demonstrating their problem-solving skills.
                
                Key Elements:

                Problem: {problem}

                Interview Process (need to follow these all):

                1. Introduction and Clarification:
                - The interviewer introduces the problem and provides the examples.
                - The interviewee need to ask for clarifications on the problem statement.
                
                2. Initial Thoughts and Approach:
                - The interviewee explains their initial thoughts and possible approaches to solve the problem.
                - The interviewer may ask questions to explore the interviewee's understanding of time and space complexity.
                
                3. Coding:
                - The interviewee writes the code to solve the problem, explaining their logic as they go.
                - The interviewer may ask the interviewee to consider different cases, such as empty arrays or arrays with no intersection.
                
                4. Testing and Optimization:
                - The interviewee dry run their code by explaining the code with provided examples and considers additional test cases.
                - The interviewer may ask about possible optimizations or alternative approaches.
                
                Wrap-Up:
                - The interviewer provides feedback on the solution, highlighting strengths and areas for improvement.
                - The interviewee reflects on their performance and discusses what they could have done differently.

            """

    openai = init_openai_config()

    messages = [{
        "role": "system",
        "content": prompt
        }]


    response = openai.chat.completions.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
    )

    response = response.choices[0].message.content
    return response

def generate_tts(text):
    openai = init_openai_config()
    # Send a request to the OpenAI TTS API to generate audio from text
    tts_response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="opus"
    )

    return tts_response.content


def generate_tts_from_generated_simulation(data):
    for item in data:
        audio = generate_tts(item['content'])
        audio_base64 = base64.b64encode(audio).decode('utf-8')
        item['audio_base64'] = audio_base64

        print(item['content'], audio_base64)
       
    return data

 

