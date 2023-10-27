# File: api/modules/db.py

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import setup_logging
from datetime import datetime

# Initialize logging
setup_logging()

# Load .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'default_db_name')

# Setup MongoDB client
client = AsyncIOMotorClient(Config.MONGO_HOST)
db = client[Config.DB_NAME]

# Setup collection
collection_users = db["users"]
collection_config = db["configurations"]
collection_webdata = db["webdatas"]

# Users function
async def save_user(user_data):
    try:
        user_data.update({
            "user_profile_picture": "",
            "register_date": datetime.utcnow(),
            "status": "active",
            "two_factor": "disabled",
            "two_factor_token": ""
        })
        result = await collection_users.insert_one(user_data)
    except Exception as e:
        print(f"Failed to insert user: {e}")
        raise

async def fetch_all_users():
    cursor = collection_users.find()
    users = []
    async for document in cursor:
        document["_id"] = str(document["_id"])
        document.pop('password', None)  # Remove the 'password' field
        document.pop('_id', None)  # Remove the 'password' field
        users.append(document)
    return users

async def get_user_by_email(email: str):
    document = await collection_users.find_one({"email": email})
    if document is not None:
        document["_id"] = str(document["_id"])
    return document

async def get_user_count():
    try:
        count = await collection_users.count_documents({})
        return count
    except Exception as e:
        print(f"Failed to get user count: {e}")
        raise