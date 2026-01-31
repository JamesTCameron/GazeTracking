# GazeTracking Backend API

Flask-based RESTful API for the GazeTracking system.

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health`
- Returns the health status of the API

### Get Metrics
- **GET** `/api/metrics`
- Returns current gaze tracking metrics in JSON format
- Response:
  ```json
  {
    "leftPupil": {"x": 123, "y": 456},
    "rightPupil": {"x": 234, "y": 567},
    "horizontal": 0.5,
    "vertical": 0.5
  }
  ```

### Video Feed (Streaming)
- **GET** `/api/video-feed`
- Returns a continuous video stream using multipart/x-mixed-replace
- Use with HTML `<img>` tag: `<img src="http://localhost:5000/api/video-feed" />`

### Single Frame with Metrics
- **GET** `/api/frame`
- Returns a single frame (base64 encoded) with metrics
- Response:
  ```json
  {
    "frame": "base64_encoded_image_data",
    "metrics": {
      "leftPupil": {"x": 123, "y": 456},
      "rightPupil": {"x": 234, "y": 567},
      "horizontal": 0.5,
      "vertical": 0.5
    }
  }
  ```

## Communication Protocol

The API uses two approaches for real-time data:

1. **HTTP Streaming (Multipart)**: For video feed using `/api/video-feed`
2. **REST Polling**: For metrics using `/api/metrics` (frontend polls at regular intervals)
3. **Single Request**: Combined frame + metrics using `/api/frame`

For production, consider implementing WebSocket connections for more efficient real-time communication.
