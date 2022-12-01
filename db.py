from pymongo import MongoClient
from dotenv import load_dotenv
from os import environ
load_dotenv()

def get_database():
    client = MongoClient(environ['MONGO_URL'])
    db = client.main
    return db