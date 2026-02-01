import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [metrics, setMetrics] = useState({
    leftPupil: { x: null, y: null },
    rightPupil: { x: null, y: null },
    horizontal: null,
    vertical: null
  });
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);

  // API base URL
  const API_URL = 'http://localhost:5000';

  // Check API health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/health`);
        if (response.data.status === 'healthy') {
          setIsConnected(true);
          setError(null);
        }
      } catch (err) {
        setIsConnected(false);
        setError('Unable to connect to API. Make sure the backend is running.');
      }
    };

    checkHealth();
  }, []);

  // Poll for metrics every 100ms
  useEffect(() => {
    if (!isConnected) return;

    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${API_URL}/api/metrics`);
        setMetrics(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch metrics');
      }
    }, 100);

    return () => clearInterval(interval);
  }, [isConnected]);

  const formatValue = (value) => {
    if (value === null || value === undefined) {
      return 'N/A';
    }
    if (typeof value === 'number') {
      return value.toFixed(4);
    }
    return value;
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>GazeTracking System</h1>
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '● Connected' : '● Disconnected'}
        </div>
      </header>

      <div className="main-content">
        <div className="video-section">
          <h2>Camera Feed</h2>
          {isConnected ? (
            <img
              src={`${API_URL}/api/video-feed`}
              alt="Live camera feed"
              className="video-feed"
            />
          ) : (
            <div className="video-placeholder">
              <p>Camera feed unavailable</p>
              <p className="error-message">{error}</p>
            </div>
          )}
        </div>

        <div className="metrics-panel">
          <h2>Gaze Metrics</h2>

          <div className="metric-group">
            <h3>Left Pupil</h3>
            <div className="metric-item">
              <span className="metric-label">X:</span>
              <span className="metric-value">{formatValue(metrics.leftPupil?.x)}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Y:</span>
              <span className="metric-value">{formatValue(metrics.leftPupil?.y)}</span>
            </div>
          </div>

          <div className="metric-group">
            <h3>Right Pupil</h3>
            <div className="metric-item">
              <span className="metric-label">X:</span>
              <span className="metric-value">{formatValue(metrics.rightPupil?.x)}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Y:</span>
              <span className="metric-value">{formatValue(metrics.rightPupil?.y)}</span>
            </div>
          </div>

          <div className="metric-group">
            <h3>Gaze Direction</h3>
            <div className="metric-item">
              <span className="metric-label">Horizontal:</span>
              <span className="metric-value">{formatValue(metrics.horizontal)}</span>
              <div className="metric-description">
                (0.0 = right, 0.5 = center, 1.0 = left)
              </div>
            </div>
            <div className="metric-item">
              <span className="metric-label">Vertical:</span>
              <span className="metric-value">{formatValue(metrics.vertical)}</span>
              <div className="metric-description">
                (0.0 = top, 0.5 = center, 1.0 = bottom)
              </div>
            </div>
          </div>

          <div className="visual-indicator">
            <h3>Visual Indicator</h3>
            <div className="gaze-grid">
              {metrics.horizontal !== null && metrics.vertical !== null ? (
                <div
                  className="gaze-dot"
                  style={{
                    left: `${(1 - metrics.horizontal) * 100}%`,
                    top: `${metrics.vertical * 100}%`
                  }}
                />
              ) : null}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
