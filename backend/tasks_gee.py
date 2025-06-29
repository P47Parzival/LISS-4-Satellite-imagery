# backend/tasks_gee.py

import ee
from celery_config import celery_app
from database import aois_collection
from bson import ObjectId
from utils import serialize_doc 
from database import sync_aois_collection

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
    aoi_document = sync_aois_collection.find_one({"_id": ObjectId(aoi_id)})
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
    # all_aois = aois_collection.find({})
    all_aois = sync_aois_collection.find({})
    
    for aoi in all_aois:
        aoi_id = str(aoi["_id"])
        print(f"Dispatching GEE task for AOI: {aoi['name']} ({aoi_id})")
        
        # This is non-blocking. It just adds the job to the Redis queue.
        process_aoi_for_changes.delay(aoi_id)
        
    return "All AOI checks have been scheduled."


# This is the actual GEE logic (slightly modified from before to return results)
def get_change_for_aoi(aoi_document: dict):
    import ee

    # 1. Extract geometry
    aoi_geometry = ee.Geometry(aoi_document["geojson"]["geometry"])

    # 2. Define time ranges (example)
    t1_range = ('2019-01-08', '2023-03-14')
    t2_range = ('2024-11-01', '2025-04-30')

    # 3. Cloud masking function for Sentinel-2
    def mask_s2_clouds(image):
        qa = image.select('QA60')
        cloudBitMask = 1 << 10
        cirrusBitMask = 1 << 11
        mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(
            qa.bitwiseAnd(cirrusBitMask).eq(0)
        )
        return image.updateMask(mask).divide(10000)

    # 4. Get image collections
    image_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(aoi_geometry)
    t1_collection = image_collection.filterDate(*t1_range)
    t2_collection = image_collection.filterDate(*t2_range)

    print(f"DEBUG: Found {t1_collection.size().getInfo()} images for T1.")
    print(f"DEBUG: Found {t2_collection.size().getInfo()} images for T2.")

    # 5. Median composite and NDVI calculation
    image_t1 = t1_collection.map(mask_s2_clouds).median().clip(aoi_geometry)
    image_t2 = t2_collection.map(mask_s2_clouds).median().clip(aoi_geometry)

    ndvi_t1 = image_t1.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ndvi_t2 = image_t2.normalizedDifference(['B8', 'B4']).rename('NDVI')

    # 6. Change detection
    ndvi_delta = ndvi_t2.subtract(ndvi_t1)
    significant_change_map = ndvi_delta.lt(-0.25)  # Threshold for loss
    final_change = significant_change_map.updateMask(significant_change_map)

    # 7. Area calculation
    area_of_change = final_change.multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=aoi_geometry,
        scale=10,
        maxPixels=1e9
    )

    print("DEBUG: Requesting change area from GEE...")
    change_area_sq_meters = area_of_change.getInfo().get('NDVI', 0)
    print(f"DEBUG: Raw change area calculated by GEE: {change_area_sq_meters} sq meters.")

    if change_area_sq_meters and change_area_sq_meters > 500:
        print(f"SUCCESS: Significant change of {change_area_sq_meters} sq meters detected.")
        return {
            "significant_change_detected": True,
            "area_sq_meters": change_area_sq_meters
        }
    else:
        print(f"INFO: No significant change detected (Area: {change_area_sq_meters} sq meters).")
        return {"significant_change_detected": False}