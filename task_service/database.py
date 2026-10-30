import os
from pymongo import MongoClient

mongo_uri = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(mongo_uri)

db = client["taskmanager"]

tasks_collection = db["tasks"]


if __name__ == "__main__":
    client.admin.command("ping")
    print("MongoDB connection successful!")
#Last three lines are used to test the connection to the MongoDB server. The "ping" command is sent to the server, and if the connection is successful, a message is printed to the console.