import jwt
from datetime import datetime, timedelta
import os

def generate_jwt_token(payload, expiration_time_minutes=120):
    """
    Generate a JWT token based on the given payload.
    
    Args:
        payload (dict): The payload to be encoded into the token.
        secret_key (str): The secret key used for encoding the token.
        expiration_time_minutes (int): Expiration time of the token in minutes.
    
    Returns:
        str: JWT token.
    """
    # Set the expiration time
    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_time_minutes)
    
    # Add the expiration time to the payload
    payload['exp'] = expiration_time
    
    secret_key = os.getenv('JWT_SECRET_KEY')

    # Generate the JWT token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return token

def verify_and_extract_payload(jwt_token):
    """
    Verify the JWT token and extract the payload.
    
    Args:
        jwt_token (str): The JWT token to verify and extract payload from.
        secret_key (str): The secret key used for decoding the token.
    
    Returns:
        dict: Payload extracted from the JWT token if verification is successful, None otherwise.
    """

    secret_key = os.getenv('JWT_SECRET_KEY')
    try:
        # Decode the JWT token
        payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token.")
    
    return None