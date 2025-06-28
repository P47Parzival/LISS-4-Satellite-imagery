# backend/tasks_gee.py

import ee
from celery_config import celery_app
from database import aois_collection # Assuming you have aoi_collection in database.py
from bson import ObjectId
from utils import serialize_doc # Assuming you have a function to serialize MongoDB docs

# Initialize GEE (it's safe to do this at the module level for a worker)
try:
    ee.Initialize(project='bah-2025') 
except Exception:
    ee.Authenticate()
    ee.Initialize(project='bah-2025')

# --- The Main GEE Processing Task ---
# The @celery_app.task decorator registers this function as a background task.
@celery_app.task
def process_aoi_for_changes(aoi_id: str):
    """
    Fetches a single AOI by its ID and runs the GEE change detection logic.
    This is where the code from the previous answer goes.
    """
    print(f"Starting GEE processing for AOI ID: {aoi_id}")
    
    # Fetch the AOI document from MongoDB
    aoi_document = aois_collection.find_one({"_id": ObjectId(aoi_id)})
    if not aoi_document:
        print(f"Error: AOI with ID {aoi_id} not found.")
        return

    # The GEE code from the previous response fits perfectly here.
    # For clarity, it's encapsulated in its own function.
    results = get_change_for_aoi(serialize_doc(aoi_document))
    
    # Here, 'results' would contain info like change_area, image_urls etc.
    if results and results["significant_change_detected"]:
        print(f"Significant change found for AOI: {aoi_document['name']}. Triggering alert.")
        # TODO: Add your alerting logic here (Step 7)
        # For example: send_email_alert(aoi_document['userId'], results)
    else:
        print(f"No significant change found for AOI: {aoi_document['name']}.")

    return f"Processing complete for {aoi_id}."


# --- The Scheduled Task Controller ---
# This task is run by Celery Beat according to the schedule in celery_config.py
@celery_app.task
def schedule_all_aoi_checks():
    """
    Queries the database for all AOIs and triggers individual processing tasks.
    """
    print("Scheduler running: Fetching all AOIs for daily check...")
    
    # In a real app, you'd filter by 'monitoringFrequency'
    # For now, let's just get all of them.
    all_aois = aois_collection.find({})
    
    for aoi in all_aois:
        aoi_id = str(aoi["_id"])
        print(f"Dispatching GEE task for AOI: {aoi['name']} ({aoi_id})")
        
        # This is non-blocking. It just adds the job to the Redis queue.
        process_aoi_for_changes.delay(aoi_id)
        
    return "All AOI checks have been scheduled."


# This is the actual GEE logic (slightly modified from before to return results)
def get_change_for_aoi(aoi_document: dict):
    # ... [The entire 'get_change_for_aoi' function from the previous response] ...
    # ... from 'aoi_geometry = ee.Geometry(geojson_aoi)' onwards ...
    
    # At the end, instead of just printing, return a dictionary
    if change_area_sq_meters and change_area_sq_meters > 500:
        return {
            "significant_change_detected": True,
            "area_sq_meters": change_area_sq_meters,
            # "t1_thumb_url": rgb_t1.getThumbURL(...)
        }
    else:
        return {"significant_change_detected": False}