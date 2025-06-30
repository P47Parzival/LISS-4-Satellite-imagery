from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from models import UserCreate, UserLogin
from database import users_collection
from utils import serialize_doc
from datetime import datetime, timedelta
import bcrypt
import jwt
from bson import ObjectId

router = APIRouter(prefix="/auth")
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days
security = HTTPBearer()

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

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):
    token = None
    # 1. Try Authorization header
    if credentials:
        token = credentials.credentials
    # 2. Try cookie
    elif "access_token" in request.cookies:
        token = request.cookies["access_token"]
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/signup")
async def signup(user_data: UserCreate):
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
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
    access_token = create_access_token(data={"sub": user_id})
    user_response = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name
    }
    response = JSONResponse({"token": access_token, "user": user_response})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",  # or "none" if using HTTPS and cross-site
        secure=False     # True if using HTTPS
    )
    return response

@router.post("/login")
async def login(user_data: UserLogin):
    user = await users_collection.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    user_id = str(user["_id"])
    access_token = create_access_token(data={"sub": user_id})
    user_response = {
        "id": user_id,
        "email": user["email"],
        "name": user.get("name")
    }
    response = JSONResponse({"token": access_token, "user": user_response})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",  # or "none" if using HTTPS and cross-site
        secure=False     # Set to True in production with HTTPS
    )
    return response

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user_response = {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "name": current_user.get("name")
    }
    return {"user": user_response}