# FastAPI Distance Calculation Service

This is a FastAPI application that calculates the driving distance and duration between two locations using the OpenRouteService API. The application accepts origin and destination coordinates in the format "latitude,longitude".

## Features

- Calculate driving distance and duration using OpenRouteService.
- Accepts coordinates in "latitude,longitude" format.
- Logs requests and responses to a file.

## Prerequisites

- Docker
- Docker Compose
- OpenRouteService API Key (You can get it [here](https://openrouteservice.org/dev/#/home))

## Setup

1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. Create a `.env` file in the root directory and add your OpenRouteService API key:
    ```env
    OPENROUTESERVICE_API_KEY=your_openrouteservice_api_key_here
    ```

3. Build and run the Docker container:
    ```bash
    docker-compose up --build
    ```

4. The application will be available at `http://localhost:8000`.

## Endpoints

### Calculate Distance

- **URL**: `/distance/`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
    ```json
    {
      "origin": "latitude,longitude",
      "destination": "latitude,longitude"
    }
    ```
- **Response**:
    ```json
    {
      "origin": "latitude,longitude",
      "destination": "latitude,longitude",
      "distance_km": distance_in_kilometers,
      "duration_min": duration_in_minutes
    }
    ```

### Example

**Request**:
```json
{
  "origin": "49.604332218782226, 6.122092153397383",
  "destination": "49.50650712862457, 5.9742027447824935"
}
