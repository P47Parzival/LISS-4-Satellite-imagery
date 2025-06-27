from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
from bson import ObjectId
import json

app = FastAPI(title="Satellite Monitoring API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "satellite_monitoring"

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
users_collection = database.users
aois_collection = database.aois

# JWT configuration
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

security = HTTPBearer()

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class AOICreate(BaseModel):
    name: str
    geojson: dict
    changeType: str
    monitoringFrequency: str
    confidenceThreshold: int
    emailAlerts: bool = True
    inAppNotifications: bool = True
    description: Optional[str] = None
    status: str = "active"

class AOIUpdate(BaseModel):
    name: Optional[str] = None
    changeType: Optional[str] = None
    monitoringFrequency: Optional[str] = None
    confidenceThreshold: Optional[int] = None
    emailAlerts: Optional[bool] = None
    inAppNotifications: Optional[bool] = None
    description: Optional[str] = None
    status: Optional[str] = None

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if key == "_id":
                result[key] = str(value)
            elif isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = serialize_doc(value)
            elif isinstance(value, list):
                result[key] = serialize_doc(value)
            else:
                result[key] = value
        return result
    return doc

# Authentication endpoints
@app.post("/auth/signup")
async def signup(user_data: UserCreate):
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    user_doc = {
        "email": user_data.email,
        "password": hashed_password,
        "name": user_data.name,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    
    # Return user data and token
    user_response = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name
    }
    
    return {"token": access_token, "user": user_response}

@app.post("/auth/login")
async def login(user_data: UserLogin):
    # Find user by email
    user = await users_collection.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    user_id = str(user["_id"])
    access_token = create_access_token(data={"sub": user_id})
    
    # Return user data and token
    user_response = {
        "id": user_id,
        "email": user["email"],
        "name": user.get("name")
    }
    
    return {"token": access_token, "user": user_response}

@app.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user_response = {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "name": current_user.get("name")
    }
    return {"user": user_response}

# AOI endpoints
@app.post("/aois/")
async def create_aoi(aoi_data: AOICreate, current_user: dict = Depends(get_current_user)):
    aoi_doc = {
        "userId": ObjectId(current_user["_id"]),
        "name": aoi_data.name,
        "geojson": aoi_data.geojson,
        "changeType": aoi_data.changeType,
        "monitoringFrequency": aoi_data.monitoringFrequency,
        "confidenceThreshold": aoi_data.confidenceThreshold,
        "emailAlerts": aoi_data.emailAlerts,
        "inAppNotifications": aoi_data.inAppNotifications,
        "description": aoi_data.description,
        "status": aoi_data.status,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
        "lastMonitored": None
    }
    
    result = await aois_collection.insert_one(aoi_doc)
    aoi_doc["_id"] = result.inserted_id
    
    return serialize_doc(aoi_doc)

@app.get("/aois/")
async def get_aois(current_user: dict = Depends(get_current_user)):
    cursor = aois_collection.find({"userId": ObjectId(current_user["_id"])})
    aois = await cursor.to_list(length=100)
    return serialize_doc(aois)

@app.get("/aois/{aoi_id}")
async def get_aoi(aoi_id: str, current_user: dict = Depends(get_current_user)):
    try:
        aoi = await aois_collection.find_one({
            "_id": ObjectId(aoi_id),
            "userId": ObjectId(current_user["_id"])
        })
        if not aoi:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        return serialize_doc(aoi)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid AOI ID")

@app.put("/aois/{aoi_id}")
async def update_aoi(aoi_id: str, aoi_data: AOIUpdate, current_user: dict = Depends(get_current_user)):
    try:
        update_data = {k: v for k, v in aoi_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        result = await aois_collection.update_one(
            {"_id": ObjectId(aoi_id), "userId": ObjectId(current_user["_id"])},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        updated_aoi = await aois_collection.find_one({
            "_id": ObjectId(aoi_id),
            "userId": ObjectId(current_user["_id"])
        })
        
        return serialize_doc(updated_aoi)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid AOI ID")

@app.delete("/aois/{aoi_id}")
async def delete_aoi(aoi_id: str, current_user: dict = Depends(get_current_user)):
    try:
        result = await aois_collection.delete_one({
            "_id": ObjectId(aoi_id),
            "userId": ObjectId(current_user["_id"])
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        return {"message": "AOI deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid AOI ID")

@app.get("/")
async def root():
    return {"message": "Satellite Monitoring API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)