
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
import os

agentsSimulationBP = Blueprint('agentsSimulationBP', __name__)

@agentsSimulationBP.route('/agentsSimulation/getResponse/<role>', methods=['POST'])
def do_conversation(role):
    data = request.json
    print(data)

    openai = init_openai_config()

    prompt = ""

    if (role == "interviewer"):
        prompt = f"""Your a software engineer interviwer and you are conducting a coding interview
                    """
    else:
        prompt = f"""Your a interviewee and you are in a coding interview
                    """        

    messages = [{
        "role": "system",
        "content": prompt
        }]


    messages += data['messages'] # append user messages

    response = openai.chat.completions.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
    )

    response = response.choices[0].message.content
    return convert_to_json_resp(response)
