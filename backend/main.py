from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes_auth import router as auth_router
from routes_aoi import router as aoi_router

import ee 
ee.Initialize(project = 'isro-bah-2025')  # Initialize Earth Engine

app = FastAPI(title="Satellite Monitoring API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(aoi_router)

@app.get("/")
async def root():
    return {"message": "Satellite Monitoring API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)