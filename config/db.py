from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from dotenv  import load_dotenv
import os
load_dotenv()
MEAL_COLLECTION=os.getenv("MEAL_COLLECTION")
USER_COLLECTION=os.getenv("USER_COLLECTION")
DB_URL=os.getenv("DATABASE_URL")
DB_NAME=os.getenv("DB_NAME")
JOB_COLLECTION=os.getenv("JOB_COLLECTION")
SERVER_TIMEZONE=os.getenv("SERVER_TIMEZONE")

class Database:
    mongo_client=None
    db=None
    @classmethod
    def db_connect(cls):
        try:
            
            cls.mongo_client=MongoClient(DB_URL)
            cls.db=cls.mongo_client[DB_NAME]
            cls.mongo_client.admin.command('ping')
            print("Connected to MongoDB successfully!")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            raise

    @classmethod
    def db_close(cls):
        if cls.mongo_client:
            cls.mongo_client.close()
            print("MongoDB connection closed")

    @classmethod
    def get_collection(cls,collection_name:str):
        if cls.mongo_client:
            return cls.db[collection_name]
            



