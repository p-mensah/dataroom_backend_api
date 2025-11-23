"""
Initializes the MongoDB database connection and collections.

This module sets up the connection to the MongoDB server using the URL
defined in the application's settings. It also provides easy access to
the different collections used throughout the application.
"""
from pymongo import MongoClient
from config import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

# Collections
access_requests_collection = db["access_requests"]
access_tokens_collection = db["access_tokens"]
admin_users_collection = db["admin_users"]
audit_logs_collection = db["audit_logs"]