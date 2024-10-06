
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
import os
import json
import base64

generateSimulationBP = Blueprint('generateSimulationBP', __name__)

@generateSimulationBP.route('/generateSimulation', methods=['POST'])
def generate_static_simulation():
    data = request.json
    problem_index = int(data['problem_index'])
    print(problem_index)
    with open(f'routes/static/problem_{problem_index}_with_audio.json', 'r') as file:
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
                Do not use built-in library if possible.

                Format your answer into a json format:
                [{{"role(interviewer/ interviewee)": "", "content": "", "code (containing STEP BY STEP CODE that the interviewee write while think aloud, only when the role is interviewee)": "","explanation (when the role is interviewee, explain the importance or rationale of answering in a such way)": ""}}, ...]]

                The interviewer may implicitly ask probing questions to understand the interviewee's thought process, while the interviewee should clearly explain their approach, consider edge cases, and write code to solve the problem.

                The interviewer may offer hints if the interviewee gets stuck and should evaluate the solution's correctness, efficiency, and clarity. The interviewee should think aloud, asking clarifying questions if needed and demonstrating their problem-solving skills.
                
                Key Elements:

                Problem: {problem}

                The interview should implicitly follow these six steps:

                1. Understanding:
                - The interviewer introduces the problem and provides examples.
                - The interviewee may asks clarifying questions to ensure a full understanding of the problem.
                - The interviewee may propose an initial test case to demonstrate their understanding of the requirements.

                2. Initial Ideation:
                - The interviewee brainstorms initial ideas on how to solve the problem.
                
                3. Idea Justification:
                - The interviewee justifies their chosen approach, explaining why it is suitable for the problem.

                4. Implementation:
                - The interviewee writes the code to solve the problem, explaining their logic as they go.
                - The interviewer may ask the interviewee to consider different cases, such as empty inputs or edge scenarios.

                5. Review (Dry Run):
                - After coding, the interviewee dry-runs their code with provided examples, walking through the logic step by step.
                - The interviewee considers additional test cases to ensure robustness.

                6. Evaluation:
                - The interviewee evaluates their solution, discussing possible optimizations, edge cases, and any necessary improvements.
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
        temperature=1,
    )

    response = response.choices[0].message.content
    return response

def generate_tts(text, role):
    openai = init_openai_config()
    # Send a request to the OpenAI TTS API to generate audio from text
    tts_response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy" if role == "interviewer" else "nova",
        input=text,
        response_format="opus"
    )

    return tts_response.content


def generate_tts_from_generated_simulation(data):
    for item in data:
        audio = generate_tts(item['content'], item['role'])
        audio_base64 = base64.b64encode(audio).decode('utf-8')
        item['audio_base64'] = audio_base64

        print(item['content'], audio_base64)
       
    return data

 

