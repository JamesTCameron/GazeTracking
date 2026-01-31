"""
Flask RESTful API for GazeTracking
Provides endpoints for camera feed and gaze metrics
"""

from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import json
import base64
import sys
import os

# Add parent directory to path to import gaze_tracking
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gaze_tracking import GazeTracking

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize gaze tracking
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'GazeTracking API'
    })


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get current gaze tracking metrics"""
    _, frame = webcam.read()

    if frame is None:
        return jsonify({
            'error': 'Failed to capture frame from webcam'
        }), 500

    # Process frame with gaze tracking
    gaze.refresh(frame)

    # Extract metrics
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    horizontal = gaze.horizontal_ratio()
    vertical = gaze.vertical_ratio()

    metrics = {
        'leftPupil': {
            'x': left_pupil[0] if left_pupil else None,
            'y': left_pupil[1] if left_pupil else None
        },
        'rightPupil': {
            'x': right_pupil[0] if right_pupil else None,
            'y': right_pupil[1] if right_pupil else None
        },
        'horizontal': horizontal,
        'vertical': vertical,
        'timestamp': None  # Could add timestamp if needed
    }

    return jsonify(metrics)


def generate_frames():
    """Generator function to yield video frames"""
    while True:
        success, frame = webcam.read()

        if not success:
            break

        # Process frame with gaze tracking
        gaze.refresh(frame)
        annotated_frame = gaze.annotated_frame()

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        # Yield frame in multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/api/video-feed', methods=['GET'])
def video_feed():
    """Video streaming endpoint using multipart/x-mixed-replace"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/api/frame', methods=['GET'])
def get_frame():
    """Get a single annotated frame with metrics as JSON"""
    _, frame = webcam.read()

    if frame is None:
        return jsonify({
            'error': 'Failed to capture frame from webcam'
        }), 500

    # Process frame with gaze tracking
    gaze.refresh(frame)
    annotated_frame = gaze.annotated_frame()

    # Get metrics
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    horizontal = gaze.horizontal_ratio()
    vertical = gaze.vertical_ratio()

    # Encode frame as base64
    ret, buffer = cv2.imencode('.jpg', annotated_frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        'frame': frame_base64,
        'metrics': {
            'leftPupil': {
                'x': left_pupil[0] if left_pupil else None,
                'y': left_pupil[1] if left_pupil else None
            },
            'rightPupil': {
                'x': right_pupil[0] if right_pupil else None,
                'y': right_pupil[1] if right_pupil else None
            },
            'horizontal': horizontal,
            'vertical': vertical
        }
    })


if __name__ == '__main__':
    # Run on localhost:5000
    app.run(host='localhost', port=5000, debug=True, threaded=True)
