# GazeTracking Setup Guide

Comprehensive installation and troubleshooting guide for GazeTracking.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Platform-Specific Setup](#platform-specific-setup)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)
- [Configuration](#configuration)

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10+, macOS 10.13+, or Linux (Ubuntu 18.04+)
- **Python**: 3.7 or higher
- **CPU**: Dual-core 2.0 GHz
- **RAM**: 2GB
- **Webcam**: 640x480 @ 15 FPS
- **Disk Space**: 500MB (including dependencies)

### Recommended Requirements

- **CPU**: Quad-core 2.5 GHz or better
- **RAM**: 4GB or more
- **Webcam**: 1280x720 @ 30 FPS
- **Disk Space**: 1GB

### Supported Python Versions

- Python 3.7 ✅
- Python 3.8 ✅
- Python 3.9 ✅
- Python 3.10 ✅
- Python 3.11 ✅
- Python 3.12 ✅

---

## Installation Methods

### Method 1: pip (Recommended for most users)

```bash
# Clone the repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python example.py
```

### Method 2: Conda (Recommended for Windows)

```bash
# Clone the repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Create conda environment
conda env create --file environment.yml

# Activate environment
conda activate GazeTracking

# Verify installation
python example.py
```

### Method 3: Docker (For consistent environments)

```bash
# Clone the repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Build Docker image
docker build -t gazetracking .

# Run container with webcam access
docker run -it --device=/dev/video0 gazetracking
```

---

## Platform-Specific Setup

### Windows Setup

#### Prerequisites

1. **Install Python**:
   - Download from https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Install Visual C++ Build Tools** (for dlib):
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "Desktop development with C++"

3. **Install CMake**:
   - Download from: https://cmake.org/download/
   - Add to PATH

#### Installation Steps

```powershell
# Clone repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# If dlib installation fails, try:
pip install dlib-binary

# Run demo
python example.py
```

#### Common Windows Issues

**Issue: "dlib not found"**
```powershell
# Solution 1: Use pre-built binary
pip install dlib-binary

# Solution 2: Use conda
conda install -c conda-forge dlib
```

**Issue: "CMake must be installed"**
```powershell
# Install via chocolatey
choco install cmake

# Or download installer from cmake.org
```

**Issue: "Cannot open webcam"**
- Check camera permissions in Windows Settings → Privacy → Camera
- Try different camera index: `cv2.VideoCapture(1)`
- Close other apps using webcam (Skype, Teams, etc.)

---

### macOS Setup

#### Prerequisites

1. **Install Homebrew**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install dependencies**:
   ```bash
   brew install python cmake
   ```

#### Installation Steps

```bash
# Clone repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run demo
python example.py
```

#### macOS-Specific Considerations

**Apple Silicon (M1/M2/M3):**
```bash
# Use conda for better compatibility
conda env create --file environment.yml
conda activate GazeTracking
```

**Camera Permissions:**
- macOS will prompt for camera access on first run
- If denied: System Preferences → Security & Privacy → Camera
- Enable access for Terminal or your Python IDE

**Issue: "dlib build fails"**
```bash
# Install build dependencies
brew install cmake boost boost-python3

# Try again
pip install dlib
```

---

### Linux Setup (Ubuntu/Debian)

#### Prerequisites

```bash
# Update package list
sudo apt-get update

# Install Python and pip
sudo apt-get install python3 python3-pip python3-venv

# Install build tools
sudo apt-get install build-essential cmake

# Install libraries for dlib
sudo apt-get install libopenblas-dev liblapack-dev

# Install libraries for OpenCV
sudo apt-get install libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev
```

#### Installation Steps

```bash
# Clone repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run demo
python example.py
```

#### Common Linux Issues

**Issue: "Cannot open /dev/video0"**
```bash
# Check camera devices
ls -l /dev/video*

# Add user to video group
sudo usermod -a -G video $USER

# Logout and login again for changes to take effect
```

**Issue: "ImportError: libGL.so.1"**
```bash
# Install OpenGL libraries
sudo apt-get install libgl1-mesa-glx
```

**Issue: "cv2.imshow() doesn't work"**
```bash
# Install GTK
sudo apt-get install python3-tk

# Or use headless mode (save frames instead of displaying)
```

---

### Raspberry Pi Setup

#### Prerequisites

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade

# Install dependencies
sudo apt-get install python3-pip python3-venv cmake
sudo apt-get install libatlas-base-dev libhdf5-dev libhdf5-serial-dev
sudo apt-get install libqtgui4 libqt4-test
```

#### Installation Steps

```bash
# Clone repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (this may take 30+ minutes on Pi)
pip install -r requirements.txt

# Run demo
python example.py
```

#### Performance Tips for Raspberry Pi

```python
# Reduce resolution for better FPS
import cv2
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Process every Nth frame
frame_counter = 0
while True:
    _, frame = webcam.read()
    if frame_counter % 3 == 0:  # Process every 3rd frame
        gaze.refresh(frame)
    frame_counter += 1
```

---

## Troubleshooting

### Dependency Installation Issues

#### Problem: pip install fails

**Solution 1: Upgrade pip**
```bash
python -m pip install --upgrade pip setuptools wheel
```

**Solution 2: Install one at a time**
```bash
pip install numpy
pip install opencv-python
pip install dlib
```

**Solution 3: Use conda**
```bash
conda install numpy opencv dlib
```

#### Problem: dlib installation takes too long or fails

**Solution 1: Use pre-built wheels (Windows)**
```bash
pip install dlib-binary
```

**Solution 2: Install build dependencies first**
```bash
# Ubuntu/Debian
sudo apt-get install cmake libopenblas-dev liblapack-dev

# macOS
brew install cmake boost boost-python3

# Then install dlib
pip install dlib
```

**Solution 3: Use conda**
```bash
conda install -c conda-forge dlib
```

### Model File Issues

#### Problem: "shape_predictor_68_face_landmarks.dat not found"

**Solution:**
```bash
# Download the model
cd gaze_tracking/trained_models/
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

# Extract
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2

# Verify
ls -lh shape_predictor_68_face_landmarks.dat
# Should be ~99MB
```

### Webcam Access Issues

#### Problem: "Cannot open webcam" or black screen

**Solution 1: Check camera index**
```python
# Try different camera indices
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} is available")
        cap.release()
```

**Solution 2: Check permissions**
- **Windows**: Settings → Privacy → Camera
- **macOS**: System Preferences → Security & Privacy → Camera
- **Linux**: Check user is in video group: `groups $USER`

**Solution 3: Close other applications**
- Close Zoom, Skype, Teams, or other apps using webcam
- Restart computer if necessary

**Solution 4: Reinstall OpenCV**
```bash
pip uninstall opencv-python
pip install opencv-python
```

### Runtime Errors

#### Problem: "No face detected"

**Checklist:**
- [ ] Face is centered in frame
- [ ] Distance: 50-80 cm from camera
- [ ] Lighting: Ensure face is well-lit
- [ ] Head pose: Face camera directly (<30° rotation)
- [ ] Camera quality: Use 640x480 minimum resolution

**Debug code:**
```python
import cv2
import dlib

# Test face detector
detector = dlib.get_frontal_face_detector()
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    print(f"Detected {len(faces)} face(s)")

    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Face Detection Test", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

#### Problem: High CPU usage / Low FPS

**Solutions:**

1. **Reduce resolution:**
```python
frame = cv2.resize(frame, (320, 240))
gaze.refresh(frame)
```

2. **Process fewer frames:**
```python
if frame_counter % 2 == 0:
    gaze.refresh(frame)
```

3. **Check system resources:**
```bash
# Monitor CPU usage
top  # Linux/macOS
# or
taskmgr  # Windows
```

---

## Verification

### Test 1: Verify Python Installation

```bash
python --version
# Should show Python 3.7 or higher
```

### Test 2: Verify Dependencies

```python
# test_dependencies.py
try:
    import numpy
    print(f"✓ NumPy {numpy.__version__}")
except ImportError:
    print("✗ NumPy not found")

try:
    import cv2
    print(f"✓ OpenCV {cv2.__version__}")
except ImportError:
    print("✗ OpenCV not found")

try:
    import dlib
    print(f"✓ Dlib {dlib.__version__}")
except ImportError:
    print("✗ Dlib not found")
```

Run: `python test_dependencies.py`

### Test 3: Verify Webcam

```python
# test_webcam.py
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("✗ Cannot open webcam")
else:
    ret, frame = cap.read()
    if ret:
        print(f"✓ Webcam working: {frame.shape}")
    else:
        print("✗ Cannot read frame")

cap.release()
```

Run: `python test_webcam.py`

### Test 4: Run Full Demo

```bash
python example.py
```

**Expected behavior:**
- Webcam window opens
- Your face is detected (no errors in console)
- Green circles appear on your pupils
- Pupil coordinates and ratios update in real-time
- ESC key exits cleanly

---

## Configuration

### Adjusting Camera Settings

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Set resolution
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Set frame rate (if supported by camera)
webcam.set(cv2.CAP_PROP_FPS, 30)

# Verify settings
width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = webcam.get(cv2.CAP_PROP_FPS)

print(f"Camera: {width}x{height} @ {fps} FPS")
```

### Custom Thresholds

```python
# Modify gaze_tracking.py

def is_right(self):
    # Adjust threshold (default 0.35)
    return self.horizontal_ratio() <= 0.40

def is_left(self):
    # Adjust threshold (default 0.65)
    return self.horizontal_ratio() >= 0.60

def is_blinking(self):
    # Adjust blink threshold (default 3.8)
    blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
    return blinking_ratio > 4.0  # More sensitive
```

### Environment Variables

```bash
# Disable OpenCV optimizations (for debugging)
export OPENCV_VIDEOIO_DEBUG=1

# Set NumPy threads
export OMP_NUM_THREADS=4
```

---

## Getting Help

If you're still having issues:

1. **Check existing documentation:**
   - [README.md](README.md)
   - [FAQ.md](FAQ.md)
   - [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)

2. **Search existing issues:**
   - https://github.com/JamesTCameron/GazeTracking/issues

3. **Create new issue:**
   - Include: OS, Python version, error messages, steps to reproduce
   - Template: [CONTRIBUTING.md](CONTRIBUTING.md)

4. **Community discussions:**
   - https://github.com/JamesTCameron/GazeTracking/discussions

---

## Next Steps

After successful installation:

1. **Read the documentation:**
   - [API_REFERENCE.md](API_REFERENCE.md) - Learn the API
   - [EXAMPLES.md](EXAMPLES.md) - See practical examples
   - [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md) - Understand how it works

2. **Experiment:**
   - Modify `example.py`
   - Try examples from [EXAMPLES.md](EXAMPLES.md)
   - Build your own application

3. **Contribute:**
   - Report bugs
   - Suggest improvements
   - Submit pull requests
   - See [CONTRIBUTING.md](CONTRIBUTING.md)

---

*Last updated: 2026-01-30*
