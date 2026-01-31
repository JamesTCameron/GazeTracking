# GazeTracking Web Application Guide

This guide explains how to set up and use the GazeTracking web application consisting of a React frontend and Flask RESTful API backend.

## Architecture Overview

The application consists of two main components:

1. **Backend (Python/Flask)**: RESTful API that processes webcam feed and provides gaze tracking metrics
2. **Frontend (React)**: Web interface that displays camera feed and real-time metrics in a side panel

## Communication Protocol

The system uses HTTP-based communication:

- **Video Streaming**: Multipart HTTP streaming (`/api/video-feed`) for continuous video feed
- **Metrics Polling**: REST API (`/api/metrics`) polled every 100ms for real-time metrics
- **Health Check**: REST API (`/api/health`) for connection status

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check endpoint |
| `/api/metrics` | GET | Get current gaze metrics (JSON) |
| `/api/video-feed` | GET | Continuous video stream (multipart) |
| `/api/frame` | GET | Single frame with metrics (JSON + base64) |

## Setup Instructions

### Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn
- Webcam

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install npm dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

## Usage

1. Start the backend server first (it needs access to your webcam)
2. Start the frontend application
3. Grant webcam permissions when prompted
4. The interface will show:
   - **Left side**: Live camera feed with annotated pupils
   - **Right side**: Numerical metrics panel with:
     - Left pupil coordinates
     - Right pupil coordinates
     - Horizontal gaze ratio
     - Vertical gaze ratio
     - Visual gaze direction indicator

## Metrics Explanation

### Pupil Coordinates
- **X, Y values**: Pixel coordinates of pupil centers in the video frame
- **null**: Indicates pupil not detected

### Gaze Ratios
- **Horizontal Ratio**:
  - 0.0 = Looking right
  - 0.5 = Looking center
  - 1.0 = Looking left

- **Vertical Ratio**:
  - 0.0 = Looking up
  - 0.5 = Looking center
  - 1.0 = Looking down

### Visual Indicator
The gaze grid shows a green dot representing current gaze direction in 2D space.

## Troubleshooting

### Backend Issues

**Webcam not accessible**
- Ensure no other application is using the webcam
- Check webcam permissions for Python/Terminal

**Module not found errors**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Make sure you're in the correct directory

**Port 5000 already in use**
- Change the port in `backend/app.py` (line with `app.run(...)`)
- Update the API URL in `frontend/src/App.js`

### Frontend Issues

**Cannot connect to API**
- Ensure backend is running at `http://localhost:5000`
- Check browser console for CORS errors
- Verify firewall settings

**npm install fails**
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then try again

**Blank screen**
- Check browser console for errors
- Ensure all dependencies installed correctly

## Development

### Backend Development
- The Flask server runs in debug mode by default
- Changes to Python files will auto-reload the server
- API responses are in JSON format

### Frontend Development
- React hot-reloading is enabled
- Changes to JS/CSS files will update automatically
- Use browser DevTools for debugging

### Adding New Metrics

1. **Backend**: Add new metric calculation in `gaze_tracking.py`
2. **Backend**: Include it in API response in `backend/app.py`
3. **Frontend**: Update state and UI in `frontend/src/App.js`

## Production Deployment

### Backend
Consider using:
- Gunicorn or uWSGI for production WSGI server
- Nginx as reverse proxy
- SSL/TLS certificates for HTTPS

### Frontend
Build optimized production version:
```bash
cd frontend
npm run build
```

Serve the `build/` directory with any static file server.

## Future Enhancements

Potential improvements for production use:

1. **WebSocket Communication**: Replace polling with WebSocket for more efficient real-time updates
2. **Authentication**: Add user authentication and session management
3. **Recording**: Add ability to record sessions and export data
4. **Calibration UI**: Add calibration interface for personalized tracking
5. **Multi-camera**: Support multiple camera sources
6. **Data Analytics**: Historical data storage and analysis
7. **Mobile Support**: Responsive design for mobile devices

## Technical Details

### Video Streaming
Uses `multipart/x-mixed-replace` HTTP streaming:
- Browser maintains single HTTP connection
- Server continuously sends JPEG frames
- Efficient for real-time video display

### Metrics Polling
Frontend polls `/api/metrics` every 100ms:
- Provides near real-time updates
- Simple implementation
- Consider WebSocket for lower latency

### Frame Processing
Backend processes each frame:
1. Capture frame from webcam
2. Detect face using dlib
3. Extract eye regions
4. Detect pupils
5. Calculate gaze metrics
6. Annotate frame
7. Send to frontend

## License

This project is released under the MIT License. See LICENSE file for details.
