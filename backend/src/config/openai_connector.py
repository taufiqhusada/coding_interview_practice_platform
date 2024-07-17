import os
import openai

def init_openai_config():
    # please insert your openai key here
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Try to print out the result
    return openai