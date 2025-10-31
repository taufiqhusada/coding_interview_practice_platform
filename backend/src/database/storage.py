"""
Storage abstraction layer that supports both MongoDB and in-memory storage.
This allows the application to run without MongoDB for development/testing.
"""

from .db import USE_MONGODB
import datetime

# In-memory storage (used when MongoDB is not available)
_in_memory_store = {}


class StorageAdapter:
    """Adapter to abstract storage operations"""
    
    @staticmethod
    def save_interview_transcript(session_id, transcript, feedback):
        """Save interview transcript and feedback"""
        if USE_MONGODB:
            from .models import InterviewTranscript
            data = {
                'sessionID': session_id,
                'datetime': datetime.datetime.now(),
                'transcript': transcript,
                'feedback': feedback,
            }
            interview = InterviewTranscript(**data)
            interview.save()
        else:
            # Use in-memory storage
            _in_memory_store[session_id] = {
                'sessionID': session_id,
                'datetime': datetime.datetime.now(),
                'transcript': transcript,
                'feedback': feedback,
            }
    
    @staticmethod
    def get_interview_transcript(session_id):
        """Retrieve interview transcript by session ID"""
        if USE_MONGODB:
            from .models import InterviewTranscript
            try:
                interview = InterviewTranscript.objects.get(sessionID=session_id)
                return {
                    'sessionID': interview.sessionID,
                    'datetime': interview.datetime,
                    'transcript': interview.transcript,
                    'feedback': interview.feedback,
                }
            except InterviewTranscript.DoesNotExist:
                return None
        else:
            # Use in-memory storage
            return _in_memory_store.get(session_id)
    
    @staticmethod
    def session_exists(session_id):
        """Check if a session exists"""
        if USE_MONGODB:
            from .models import InterviewTranscript
            return InterviewTranscript.objects(sessionID=session_id).count() > 0
        else:
            return session_id in _in_memory_store
