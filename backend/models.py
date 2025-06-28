from pydantic import BaseModel
from typing import Optional

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