# GazeTracking Frontend

React-based frontend for the GazeTracking system with real-time camera feed and metrics display.

## Features

- Real-time camera feed display
- Side panel with numerical gaze metrics:
  - Left pupil coordinates (x, y)
  - Right pupil coordinates (x, y)
  - Horizontal gaze ratio (0.0 = right, 0.5 = center, 1.0 = left)
  - Vertical gaze ratio (0.0 = top, 0.5 = center, 1.0 = bottom)
- Visual gaze direction indicator
- Connection status indicator
- Responsive design

## Installation

```bash
cd frontend
npm install
```

## Running the Frontend

Make sure the backend API is running first, then:

```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

## Development

The frontend uses:
- React 18
- Axios for API calls
- CSS3 for styling

### API Configuration

The frontend expects the backend API to be running at `http://localhost:5000`. This is configured in `package.json` as a proxy.

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.
