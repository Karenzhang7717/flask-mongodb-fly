import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util
import certifi  # Add this import

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MongoDB Atlas connection string with SSL parameters
mongodb_uri = os.getenv('MONGODB_URI')
if not mongodb_uri:
    logger.error("No MongoDB URI found in environment variables!")
    raise ValueError("MongoDB URI not configured")

try:
    # Use certifi for SSL certificate verification
    client = MongoClient(mongodb_uri,
                        tlsCAFile=certifi.where(),  # Add SSL certificate
                        serverSelectionTimeoutMS=5000)  # Reduce timeout for faster error reporting
    
    db = client['your_database_name']  # Replace with your actual database name
    
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB!")
    
    # Create index for geospatial queries
    db.locations.create_index([("location", "2dsphere")])
    logger.info("Created 2dsphere index")
except Exception as e:
    logger.error(f"MongoDB Connection Error: {e}")
    raise

@app.route("/")
def hello_world():
    return "Hello, World! This is a Flask & MongoDB app deployed on Fly.io"

@app.route("/locations", methods=["POST"])
def add_location():
    data = request.json
    result = db.locations.insert_one(data)
    return jsonify({"message": "Location added successfully", "id": str(result.inserted_id)}), 201

@app.route("/locations", methods=["GET"])
def get_locations():
    locations = list(db.locations.find())
    return json.loads(json_util.dumps(locations))

@app.route("/nearby", methods=["GET"])
def find_nearby():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    max_distance = int(request.args.get("distance", 1000))  # Default to 1000 meters

    nearby = db.locations.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "$maxDistance": max_distance
            }
        }
    })

    return json.loads(json_util.dumps(list(nearby)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)