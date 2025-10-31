
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
from database.storage import StorageAdapter
import os
import uuid
import datetime

getFeedbackBP = Blueprint('getFeedback', __name__)

def save_transcript_and_feedback(transcript, feedback):
    # Generate a random sessionID using uuid
    session_id = str(uuid.uuid4())  
    
    # Save using storage adapter (works with or without MongoDB)
    StorageAdapter.save_interview_transcript(session_id, transcript, feedback)

    return session_id


@getFeedbackBP.route('/getFeedback/general', methods=['POST'])
def get_general_feedback():
    data = request.json
    transcript = data['transcript']


    openai = init_openai_config()

    prompt = f"""
        "I have a transcript of a coding interview where the interviewee is required to think aloud while solving a problem. Based on the transcript provided below, please give detailed feedback on the interviewee's performance, focusing on the following four aspects. Format the response in JSON with this structure:
            {{
                "understanding": "Feedback on how the interviewee demonstrated their understanding of the problem by asking clarifying questions and/or proposing a test case.",
                "initial_ideation": "Feedback on how the interviewee brainstormed and proposed their initial ideas.",
                "idea_justification": "Feedback on how the interviewee justified their proposed approach and explained why it was suitable.",
                "implementation": "Feedback on how the interviewee communicated their thought process while coding the solution.",
                "review_dry_run": "Feedback on how the interviewee performed a dry run of their code, explaining the execution flow using test cases.",
                "evaluation": "Feedback on how the interviewee evaluated their solution, including discussions of potential optimizations, edge cases, or improvements."
            }}

            make sure you assess it objectively.

            Here are the specific phases to assess:

            1. Understanding: Evaluate whether they proposed a relevant test case to demonstrate their understanding of the problem or/and how effectively the interviewee asked clarifying questions. Did they fully grasp the requirements? Were there missed opportunities to seek more clarity?

            2. Initial Ideation: Assess how the interviewee brainstormed initial ideas and solutions. Did they consider multiple approaches or stick with a single idea? Did they clearly explain their thought process?

            3. Idea Justification: Evaluate how well the interviewee justified their solution. Did they explain why their approach was suitable or compare it to alternative solutions? Were they able to defend their choice of data structures, algorithms, or logic?

            4. Implementation: Provide feedback on how well the interviewee communicated their thought process while coding. Was their reasoning easy to follow? Were there gaps in their explanation or places where communication became unclear?

            5. Review (Dry Run): Analyze how the interviewee performed a dry run of their code with a test case. Did they clearly explain the flow of execution, identify potential issues, or spot logical errors? Did they account for edge cases?

            6. Evaluation: Provide feedback on how the interviewee evaluated their solution after coding. Did they discuss possible optimizations, improvements, or additional test cases to check for edge cases?

            If the interviewee did not perform a phase, note that it was not done.
            
            Transcript:  {str(transcript)}

        """

    messages = [{
        "role": "system",
        "content": prompt
        }]

    gpt_response = openai.chat.completions.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
        response_format={ "type": "json_object" }
    )

    feedback = gpt_response.choices[0].message.content

    session_id = save_transcript_and_feedback(transcript, feedback)


    res = {'feedback': feedback, 'session_id': session_id}
    return res



@getFeedbackBP.route('/retrieveFeedback/general', methods=['POST'])
def retrieve_general_feedback():
    try:
        data = request.json
        sessionID = data['sessionID']
        
        # Retrieve using storage adapter (works with or without MongoDB)
        interview = StorageAdapter.get_interview_transcript(sessionID)
        
        if interview:
            return {
                'sessionID': interview['sessionID'],
                'datetime': interview['datetime'],
                'transcript': interview['transcript'],
                'feedback': interview['feedback'],
            }
        else:
            # Handle case where no transcript is found for the given sessionID
            return {'error': 'No transcript found for the given sessionID'}
    except Exception as e:
        return {'error': str(e)}


@getFeedbackBP.route('/getFeedback/specific', methods=['POST'])
def get_specific_feedback():
    data = request.json
    transcript = data['transcript']
    phase = data['phase']


    openai = init_openai_config()

    dict_phase = {
        "Understanding": "Understanding:  Evaluate whether they proposed a relevant test case to demonstrate their understanding of the problem or/and how effectively the interviewee asked clarifying questions. Did they fully grasp the requirements? Were there missed opportunities to seek more clarity?",

        "Initial Ideation": "Initial Ideation: Assess how the interviewee brainstormed initial ideas and solutions. Did they clearly explain their thought process?",

        "Idea Justification": "Idea Justification: Evaluate how well the interviewee justified their proposed solution. Did they explain why their approach was suitable or compare it to alternative solutions? Were they able to defend their choice of data structures, algorithms, or logic?",

        "Implementation": "Implementation: Provide feedback on how well the interviewee communicated their thought process while coding the solution. Was their logic and reasoning easy to follow? Were there gaps in their explanation or moments of unclear communication?",

        "Review (Dry Run)": "Review (Dry Run): Analyze how the interviewee performed a dry run of their code using a test case. Did they clearly explain the flow of execution, identify potential issues, or spot logical errors? Did they account for edge cases?",

        "Evaluation": "Evaluation: Provide feedback on how the interviewee evaluated their solution after coding. Did they discuss possible optimizations, improvements, or additional test cases to check for edge cases?"
    }


    prompt = f"""
        "I have a transcript of a coding interview where the interviewee is required to think aloud while solving a problem. Based on the transcript provided below, please give detailed feedback on specific phase {phase} 

            make sure you assess it objectively. 

            Here the guideline specific phases to assess:

            {dict_phase[phase]}

            If the interviewee do not do the phase above then say it that they do not do it.

            Transcript:  {str(transcript)}

            LIMIT your answer to one sentence short and concise, 30 words max.

        """

    messages = [{
        "role": "system",
        "content": prompt
        }]

    gpt_response = openai.chat.completions.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
    )

    feedback = gpt_response.choices[0].message.content


    res = {'feedback': feedback}
    return res
