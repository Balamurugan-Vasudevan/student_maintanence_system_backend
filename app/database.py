from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import certifi
import ssl

client = None
db     = None

async def connect_db():
    global client, db

    # create SSL context using certifi certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode    = ssl.CERT_NONE

    client = AsyncIOMotorClient(
        settings.MONGO_URI,
        tls                          = True,
        tlsAllowInvalidCertificates  = True,
        tlsAllowInvalidHostnames     = True,
        serverSelectionTimeoutMS     = 60000,
        connectTimeoutMS             = 60000,
        socketTimeoutMS              = 60000,
    )
    db = client[settings.DB_NAME]

    try:
        await client.admin.command('ping')
        print(f"✅ Connected to MongoDB Atlas: {settings.DB_NAME}")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise

async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_db():
    return db