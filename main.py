from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import openrouteservice
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, filename='/app/logs/app.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Retrieve the OpenRouteService API key from the environment variable
API_KEY = os.getenv('OPENROUTESERVICE_API_KEY')
if not API_KEY:
    logger.error("The OPENROUTESERVICE_API_KEY environment variable is not set")
    raise RuntimeError("The OPENROUTESERVICE_API_KEY environment variable is not set")

client = openrouteservice.Client(key=API_KEY)

class Location(BaseModel):
    origin: str  # "latitude,longitude"
    destination: str  # "latitude,longitude"

    @validator('origin', 'destination')
    def check_coordinates(cls, v):
        parts = v.split(',')
        if len(parts) != 2:
            raise ValueError('Coordinates must be in the format "latitude,longitude"')
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
        except ValueError:
            raise ValueError('Latitude and Longitude must be valid float numbers')
        return [lon, lat]  # return as [longitude, latitude] for openrouteservice

@app.post("/distance/")
async def get_distance(location: Location):
    try:
        logger.info(f"Received request: origin={location.origin}, destination={location.destination}")
        
        origin_coords = location.origin
        destination_coords = location.destination
        
        # Request directions from OpenRouteService
        routes = client.directions(
            coordinates=[origin_coords, destination_coords],
            profile='driving-car',
            format='geojson'
        )

        # Extract distance and duration
        distance = routes['features'][0]['properties']['segments'][0]['distance'] / 1000  # Convert to km
        ## distance round to 2 decimal places
        distance = round(distance, 2)
        duration = routes['features'][0]['properties']['segments'][0]['duration'] / 60  # Convert to minutes
        ## duration round to 0 decimal places
        duration = round(duration, 0)

        logger.info(f"Calculated distance: {distance} km, duration: {duration} min")

        return {
            "origin": location.origin,
            "destination": location.destination,
            "distance_km": distance,
            "duration_min": duration
        }
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
