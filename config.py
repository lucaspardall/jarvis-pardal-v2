import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
webhook_make = os.getenv('WEBHOOK_MAKE')