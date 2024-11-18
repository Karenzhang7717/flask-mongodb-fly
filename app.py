import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)

# MongoDB Atlas connection string
mongodb_uri = os.environ.get("MONGODB_URI")
client = MongoClient(mongodb_uri)
db = client.get_database()

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
    app.run(host="0.0.0.0", port=8080) #change to your ip address
