from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "satellite_monitoring"

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
users_collection = database.users
aois_collection = database.aois