from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")

if secret_key is None:
    raise ValueError("SECRET_KEY not found!")

SECRET_KEY = secret_key.encode() 
JWT_ISSUER = "notes-api"
EXPIRY_TOKEN = (15*60) # 15 mins