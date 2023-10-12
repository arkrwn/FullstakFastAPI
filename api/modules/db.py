# File: api/modules/db.py

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'default_db_name')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'default_collection_name')

# Setup MongoDB client
client = AsyncIOMotorClient(Config.MONGO_HOST)
db = client[Config.DB_NAME]
collection = db[Config.COLLECTION_NAME]

async def save_user(user_data):
    try:
        result = await collection.insert_one(user_data)
    except Exception as e:
        print(f"Failed to insert user: {e}")
        raise

async def fetch_all_users():
    cursor = collection.find()
    users = []
    async for document in cursor:
        document["_id"] = str(document["_id"])  # Convert ObjectId to str
        users.append(document)
    return users

# Updated get_user_by_email function
async def get_user_by_email(email: str):
    document = await collection.find_one({"email": email})
    if document is not None:
        document["_id"] = str(document["_id"])  # Convert ObjectId to str
    return document
