import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("TEST_NEW2"))
arr = os.listdir()
print(arr)