from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
db     = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db     = client[settings.DB_NAME]

    # verify connection
    try:
        await client.admin.command('ping')
        print(f"Connected to MongoDB Atlas: {settings.DB_NAME}")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise

async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_db():
    return db