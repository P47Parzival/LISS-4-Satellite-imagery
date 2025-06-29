from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "satellite_monitoring"

from pymongo import MongoClient

sync_client = MongoClient(MONGODB_URL)
sync_database = sync_client[DATABASE_NAME]
sync_aois_collection = sync_database.aois
sync_users_collection = sync_database.users
sync_changes_collection = sync_database.changes  # Add this line for sync access

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
users_collection = database.users
aois_collection = database.aois
changes_collection = database.changes           # Add this line for async access (if needed)
