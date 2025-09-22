import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COGNITO_CLIENT_ID=os.getenv("COGNITO_CLIENT_ID")
USER_POOL_ID=os.getenv("USER_POOL_ID")
COGNITO_REGION=os.getenv("COGNITO_REGION")
