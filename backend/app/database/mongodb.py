
from pymongo import MongoClient

from backend.app.core.config import settings


def create_mongodb_client():

    client = MongoClient(
        settings.MONGODB_URL,
        serverSelectionTimeoutMS=5000
    )

    client.admin.command("ping")

    return client
