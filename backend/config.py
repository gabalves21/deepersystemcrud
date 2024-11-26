from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load the variables from the .env file
load_dotenv()

# Get the connection URI from the .env file
uri = os.getenv("DATABASE_URI")

# Ensure the URI is being read correctly
if not uri:
    print("ERROR: DATABASE_URI not found in the .env file.")
    exit(1)

# Create a connection to MongoDB
try:
    client = MongoClient(uri)
    print("Connection established successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit(1)

# Access the database
db = client["DeeperSytem"]
users = db.users

# Function to create the users collection with a unique index
def create_users_table():
    try:
        users.create_index([("username", 1)], unique=True)
        print("Unique index created for 'username' successfully.")
    except Exception as e:
        print(f"Failed to create index: {e}")

# Test the connection to the database
def test_connection():
    try:
        client.admin.command('ping')
        print("Pinged successfully. You are connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")

# Create the table (or index) and test the connection
create_users_table()
test_connection()
