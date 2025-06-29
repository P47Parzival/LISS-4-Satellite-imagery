from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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

class ChangeRecord(BaseModel):
    aoi_id: str
    user_id: str
    detection_date: datetime
    area_of_change: float
    before_image_url: str
    after_image_url: str
    status: str = "unread"