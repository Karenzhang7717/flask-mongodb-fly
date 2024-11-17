# flask-mongodb-fly

# Flask MongoDB Location Discovery API

A location-based discovery API built with Flask and MongoDB Atlas, deployed on Fly.io. This application demonstrates how to create a RESTful API that allows users to store, search, and discover locations using MongoDB's geospatial features.

## Features

- Store location data with geographical coordinates
- Retrieve all stored locations
- Find nearby locations based on coordinates and distance
- MongoDB Atlas integration for robust data storage
- Deployed on Fly.io for scalable hosting

## Prerequisites

- Python 3.x
- MongoDB Atlas account
- Fly.io account
- Fly CLI

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Karenzhang7717/flask-mongodb-fly.git
cd flask-mongodb-fly
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MongoDB Atlas:
   - Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a new cluster (free tier is sufficient for testing)
   - In the Security tab, create a database user and whitelist your IP address
   - Get your connection string from the Clusters tab > Connect > Connect your application

5. Create a `.env` file and add your MongoDB URI:
```bash
MONGODB_URI="your_mongodb_atlas_connection_string"
```

6. Run the application locally:
```bash
python app.py
```

## API Endpoints

### GET /
- Returns a welcome message
- Response: "Hello, World! This is a Flask & MongoDB app deployed on Fly.io"

### POST /locations
- Adds a new location
- Request body example:
```json
{
    "name": "Eiffel Tower",
    "location": {
        "type": "Point",
        "coordinates": [2.2945, 48.8584]
    }
}
```

### GET /locations
- Retrieves all stored locations
- Returns an array of location objects

### GET /nearby
- Finds locations near specified coordinates
- Query parameters:
  - lat: Latitude (float)
  - lon: Longitude (float)
  - distance: Maximum distance in meters (integer, default: 1000)
- Example: `/nearby?lat=48.8584&lon=2.2945&distance=5000`

## Deployment

1. Install the Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Sign up and log in to Fly.io:
```bash
fly auth signup
fly auth login
```

3. Set your MongoDB URI as a secret:
```bash
fly secrets set MONGODB_URI="your_mongodb_atlas_connection_string"
```

4. Deploy the application:
```bash
fly deploy
```

## Project Structure

```
flask-mongodb-fly/
├── app.py             # Main application file
├── requirements.txt   # Python dependencies
├── Procfile          # Gunicorn web server configuration
└── fly.toml          # Fly.io configuration
```

## Testing

Test the API endpoints using curl:

```bash
# Add a location
curl -X POST http://localhost:8080/locations \
  -H "Content-Type: application/json" \
  -d '{"name": "Eiffel Tower", "location": {"type": "Point", "coordinates": [2.2945, 48.8584]}}'

# Get all locations
curl http://localhost:8080/locations

# Find nearby locations
curl "http://localhost:8080/nearby?lat=48.8584&lon=2.2945&distance=5000"
```
