# Satellite Monitoring Backend

FastAPI backend for the satellite monitoring application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install and start MongoDB:
```bash
# On Ubuntu/Debian
sudo apt-get install mongodb

# On macOS with Homebrew
brew install mongodb-community
brew services start mongodb-community

# On Windows, download and install from MongoDB website
```

3. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Database Collections

### Users
- `_id`: ObjectId
- `email`: String (unique)
- `password`: String (hashed)
- `name`: String (optional)
- `createdAt`: DateTime
- `updatedAt`: DateTime

### AOIs (Areas of Interest)
- `_id`: ObjectId
- `userId`: ObjectId (reference to user)
- `name`: String
- `geojson`: Object (GeoJSON geometry)
- `changeType`: String
- `monitoringFrequency`: String
- `confidenceThreshold`: Number
- `emailAlerts`: Boolean
- `inAppNotifications`: Boolean
- `description`: String (optional)
- `status`: String
- `createdAt`: DateTime
- `updatedAt`: DateTime
- `lastMonitored`: DateTime (optional)

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```