from .config import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .config import settings

mongodb_uri = f"mongodb+srv://{settings.db_username}:{settings.db_pwd}@krispy0.x41klmh.mongodb.net/{settings.db_env}?retryWrites=true&w=majority"

def get_mongodb():
    db = MongoClient(mongodb_uri, server_api=ServerApi('1'))

    try:
        yield db.get_database()
    finally:
        db.close()