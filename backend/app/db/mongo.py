from pymongo import AsyncMongoClient
from app.core.settings import settings

client = AsyncMongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

users_col = db.get_collection("users")
