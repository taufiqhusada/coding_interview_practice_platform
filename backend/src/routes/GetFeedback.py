
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
from database.models import InterviewTranscript
import os
import uuid
import datetime

getFeedbackBP = Blueprint('getFeedback', __name__)

def save_transcript_and_feedback(transcript, feedback):
    # Generate a random sessionID using uuid
    session_id = str(uuid.uuid4())  
    # Capture the current datetime
    current_datetime = datetime.datetime.now()
    
    # Create the data object
    data = {
        'sessionID': session_id,
        'datetime': current_datetime,
        'transcript': transcript,
        'feedback': feedback,
    }
    
    # Create an InterviewTranscript object and save it
    interview = InterviewTranscript(**data)
    interview.save()

    return session_id


@getFeedbackBP.route('/getFeedback/general', methods=['POST'])
def get_general_feedback():
    data = request.json
    transcript = data['transcript']
    print(transcript)


    openai = init_openai_config()

    prompt = f"""
        "I have a transcript of a coding interview where the interviewee is required to think aloud while solving a problem. Based on the transcript provided below, please give detailed feedback on the interviewee's performance, focusing on the following four aspects. Format the response in JSON with this structure:
            {{
            "clarification": "Feedback on how the interviewee asked clarifying questions.",
            "ideation": "Feedback on how the interviewee proposed ideas and solutions.",
            "communication_during_coding": "Feedback on how the interviewee communicated while coding.",
            "dry_run": "Feedback on how the interviewee explained their code using provided examples or test cases."
            }}

            make sure you assess it objectively.

            Here are the specific phases to assess:

            1. Clarification: Evaluate how effectively the interviewee asked clarifying questions about the problem. Did they fully understand the requirements, constraints, or edge cases? Were there any missed opportunities to ask for more information?

            2. Ideation: Assess how the interviewee proposed ideas and solutions. Did they consider multiple approaches, explain their thought process clearly, and propose feasible solutions?

            3. Communication during coding: Provide feedback on how well the interviewee explained their code while writing it. Was their logic and reasoning easy to follow? Were there moments where communication broke down or became unclear?

            4. Dry run: Analyze how the interviewee walked through their code with provided examples or test cases. Did they clearly explain the flow of the code, identify potential issues, and consider additional edge cases?

            If the interviewee do not do the phases above then say it that they do not do it.

            Transcript:  {str(transcript)}

        """

    messages = [{
        "role": "system",
        "content": prompt
        }]
    print(messages)

    gpt_response = openai.chat.completions.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
        response_format={ "type": "json_object" }
    )

    feedback = gpt_response.choices[0].message.content

    session_id = save_transcript_and_feedback(transcript, feedback)

    print(feedback)

    res = {'feedback': feedback, 'session_id': session_id}
    return res



@getFeedbackBP.route('/retrieveFeedback/general', methods=['POST'])
def retrieve_general_feedback():
    try:
        data = request.json
        sessionID = data['sessionID']
        # Query the InterviewTranscript object based on sessionID
        interview = InterviewTranscript.objects.get(sessionID=sessionID)
        
        # Return the transcript and feedback
        return {
            'sessionID': interview.sessionID,
            'datetime': interview.datetime,
            'transcript': interview.transcript,
            'feedback': interview.feedback,
        }
    except InterviewTranscript.DoesNotExist:
        # Handle case where no transcript is found for the given sessionID
        return {'error': 'No transcript found for the given sessionID'}

