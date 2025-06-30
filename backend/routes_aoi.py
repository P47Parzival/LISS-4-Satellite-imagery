from fastapi import APIRouter, Depends, HTTPException, Query
from models import AOICreate, AOIUpdate
from database import aois_collection
from utils import serialize_doc
from datetime import datetime
from bson import ObjectId
from routes_auth import get_current_user
from database import sync_changes_collection
from fastapi.responses import JSONResponse
import ee

router = APIRouter(prefix="/aois")

@router.post("/")
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

@router.get("/")
async def get_aois(current_user: dict = Depends(get_current_user)):
    cursor = aois_collection.find({"userId": ObjectId(current_user["_id"])})
    aois = await cursor.to_list(length=100)
    return serialize_doc(aois)

@router.get("/{aoi_id}")
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

@router.put("/{aoi_id}")
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

@router.delete("/{aoi_id}")
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
    
@router.get("/{aoi_id}/changes")
async def get_aoi_alerts(aoi_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # print("Querying for aoi_id:", aoi_id, "user_id:", str(current_user["_id"]))
        sample = sync_changes_collection.find_one()
        # print("Sample change doc:", sample)
        alerts = list(sync_changes_collection.find({
            "aoi_id": aoi_id,
            "user_id": str(current_user["_id"])
        }).sort("detection_date", -1))
        # print("Found alerts:", alerts)
        # Ensure all ObjectIds are strings
        for alert in alerts:
            if "_id" in alert:
                alert["_id"] = str(alert["_id"])
        return alerts  # Let FastAPI handle JSON serialization
    except Exception as e:
        print("Error in get_aoi_alerts:", e)
        return []  # Always return an empty list on error
    
# Retrieving thumbnail params

def generate_thumbnail(params):
    geometry = ee.Geometry(params["geometry"])
    collection = ee.ImageCollection(params["collection"]).filterBounds(geometry).filterDate(*params["date_range"])
    image = collection.median().clip(geometry)
    vis_params = params["vis_params"]
    thumb_params = params["thumb_params"]
    url = image.visualize(**vis_params).getThumbURL(thumb_params)
    return url

@router.get("/{change_id}/thumbnail")
async def get_change_thumbnail(
    change_id: str,
    type: str = Query(..., regex="^(before|after)$"),
    current_user: dict = Depends(get_current_user)
):
    change = sync_changes_collection.find_one({"_id": ObjectId(change_id)})
    if not change:
        raise HTTPException(status_code=404, detail="Change not found")
    if change["user_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    params = change[f"{type}_image_params"]
    url = generate_thumbnail(params)
    return {"url": url}