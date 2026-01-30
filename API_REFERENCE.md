# GazeTracking API Reference

Complete API documentation for the GazeTracking library.

## Table of Contents

- [GazeTracking Class](#gazetracking-class)
- [Properties](#properties)
- [Methods](#methods)
- [Usage Examples](#usage-examples)
- [Return Value Reference](#return-value-reference)
- [Error Handling](#error-handling)

## GazeTracking Class

The main controller class for eye tracking functionality.

### Constructor

```python
from gaze_tracking import GazeTracking

gaze = GazeTracking()
```

**Description:**
Initializes the GazeTracking system with face detection and facial landmark models.

**Parameters:**
- None

**Initialization Steps:**
1. Loads Dlib's HOG face detector
2. Loads 68-point facial landmark predictor model
3. Initializes calibration system
4. Prepares Eye objects for left and right eyes

**Raises:**
- `FileNotFoundError`: If `shape_predictor_68_face_landmarks.dat` model file is missing
- `RuntimeError`: If Dlib models fail to load

**Example:**
```python
gaze = GazeTracking()
# System is now ready to process frames
```

---

## Properties

### `pupils_located`

```python
gaze.pupils_located -> bool
```

**Description:**
Checks whether both pupils have been successfully detected in the current frame.

**Returns:**
- `bool`: `True` if both pupils are located, `False` otherwise

**Example:**
```python
gaze.refresh(frame)
if gaze.pupils_located:
    print("Pupils detected!")
else:
    print("No pupils found - check lighting or face position")
```

**Use Case:**
Always check this property before accessing pupil coordinates or gaze ratios to avoid `None` values.

---

## Methods

### `refresh(frame)`

```python
gaze.refresh(frame: numpy.ndarray) -> None
```

**Description:**
Processes a new frame and updates all gaze tracking data. This is the main method you'll call in your tracking loop.

**Parameters:**
- `frame` (numpy.ndarray): BGR image from webcam or video source
  - Typical format: `(height, width, 3)` shape array
  - Recommended resolution: 640x480 or higher
  - Color space: BGR (OpenCV default)

**Returns:**
- None (updates internal state)

**Processing Pipeline:**
1. Converts frame to grayscale
2. Detects face using HOG detector
3. Extracts 68 facial landmarks
4. Isolates left and right eye regions
5. Runs calibration (first 20 frames)
6. Detects pupils in each eye
7. Updates gaze direction data

**Example:**
```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)  # Process this frame

    # Access updated gaze data
    print(gaze.horizontal_ratio())
```

**Performance:**
- Typical processing time: 40-80ms per frame
- Frame rate: 12-25 FPS on modern CPUs

**Notes:**
- Call this method once per frame
- If no face is detected, `pupils_located` will be `False`
- Calibration runs automatically during first 20 frames

---

### `pupil_left_coords()`

```python
gaze.pupil_left_coords() -> Optional[Tuple[int, int]]
```

**Description:**
Returns the absolute (x, y) coordinates of the left pupil in the original frame.

**Returns:**
- `Tuple[int, int]`: Pupil coordinates `(x, y)` in pixels
- `None`: If pupils not located

**Coordinate System:**
- Origin (0, 0) is top-left corner of frame
- x increases rightward
- y increases downward

**Example:**
```python
gaze.refresh(frame)
left_pupil = gaze.pupil_left_coords()

if left_pupil:
    x, y = left_pupil
    print(f"Left pupil at pixel ({x}, {y})")
    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Draw green dot
```

**Use Cases:**
- Drawing pupil positions on frame
- Calculating distances between pupils
- Logging absolute pupil positions
- Custom gaze analysis algorithms

---

### `pupil_right_coords()`

```python
gaze.pupil_right_coords() -> Optional[Tuple[int, int]]
```

**Description:**
Returns the absolute (x, y) coordinates of the right pupil in the original frame.

**Returns:**
- `Tuple[int, int]`: Pupil coordinates `(x, y)` in pixels
- `None`: If pupils not located

**Example:**
```python
gaze.refresh(frame)
right_pupil = gaze.pupil_right_coords()

if right_pupil:
    x, y = right_pupil
    print(f"Right pupil at pixel ({x}, {y})")
```

**Notes:**
- Coordinates are in the same reference frame as input image
- Useful for biometric measurements and pupil distance calculations

---

### `horizontal_ratio()`

```python
gaze.horizontal_ratio() -> Optional[float]
```

**Description:**
Returns a normalized ratio (0.0 to 1.0) indicating horizontal gaze direction.

**Returns:**
- `float`: Gaze ratio where:
  - `0.0` = Looking extreme right
  - `0.5` = Looking center
  - `1.0` = Looking extreme left
- `None`: If pupils not located

**Calculation:**
```python
# For each eye:
ratio = pupil_x / (eye_center_x * 2 - 10)

# Average both eyes:
horizontal_ratio = (left_ratio + right_ratio) / 2
```

**Interpretation Thresholds:**
- `≤ 0.35`: User is looking right
- `0.35 - 0.65`: User is looking center
- `≥ 0.65`: User is looking left

**Example:**
```python
gaze.refresh(frame)
h_ratio = gaze.horizontal_ratio()

if h_ratio is not None:
    if h_ratio <= 0.35:
        print("Looking RIGHT")
    elif h_ratio >= 0.65:
        print("Looking LEFT")
    else:
        print("Looking CENTER")
```

**Use Cases:**
- Gaze-based UI navigation
- Attention tracking
- Gaming controls (look to move)
- Accessibility applications

**Accuracy:**
- Typical accuracy: ±5-10° angular error
- Best in controlled lighting with frontal face

---

### `vertical_ratio()`

```python
gaze.vertical_ratio() -> Optional[float]
```

**Description:**
Returns a normalized ratio (0.0 to 1.0) indicating vertical gaze direction.

**Returns:**
- `float`: Gaze ratio where:
  - `0.0` = Looking extreme up
  - `0.5` = Looking center
  - `1.0` = Looking extreme down
- `None`: If pupils not located

**Calculation:**
```python
# For each eye:
ratio = pupil_y / (eye_center_y * 2 - 10)

# Average both eyes:
vertical_ratio = (left_ratio + right_ratio) / 2
```

**Example:**
```python
gaze.refresh(frame)
v_ratio = gaze.vertical_ratio()

if v_ratio is not None:
    if v_ratio < 0.4:
        print("Looking UP")
    elif v_ratio > 0.6:
        print("Looking DOWN")
    else:
        print("Looking CENTER (vertical)")
```

**Use Cases:**
- Vertical scrolling control
- Menu navigation
- Reading pattern analysis
- Attention heatmaps

**Notes:**
- Less accurate than horizontal tracking due to eyelid interference
- Works best with fully open eyes

---

### `is_right()`

```python
gaze.is_right() -> bool
```

**Description:**
Checks if the user is looking to the right.

**Returns:**
- `bool`: `True` if looking right, `False` otherwise

**Threshold:**
- Returns `True` when `horizontal_ratio() <= 0.35`

**Example:**
```python
gaze.refresh(frame)
if gaze.is_right():
    print("User is looking right!")
    # Trigger right action (e.g., move cursor right)
```

**Use Cases:**
- Simple directional controls
- Binary gaze decisions
- Accessibility switches

---

### `is_left()`

```python
gaze.is_left() -> bool
```

**Description:**
Checks if the user is looking to the left.

**Returns:**
- `bool`: `True` if looking left, `False` otherwise

**Threshold:**
- Returns `True` when `horizontal_ratio() >= 0.65`

**Example:**
```python
gaze.refresh(frame)
if gaze.is_left():
    print("User is looking left!")
    # Trigger left action
```

---

### `is_center()`

```python
gaze.is_center() -> bool
```

**Description:**
Checks if the user is looking at the center (horizontally).

**Returns:**
- `bool`: `True` if looking center, `False` otherwise

**Threshold:**
- Returns `True` when `0.35 < horizontal_ratio() < 0.65`

**Example:**
```python
gaze.refresh(frame)
if gaze.is_center():
    print("User is looking at center")
    # Confirm selection, etc.
```

---

### `is_blinking()`

```python
gaze.is_blinking() -> bool
```

**Description:**
Checks if the user's eyes are closed or blinking.

**Returns:**
- `bool`: `True` if eyes are closed/blinking, `False` if eyes are open

**Algorithm:**
Uses Eye Aspect Ratio (EAR):
```
EAR = eye_width / eye_height
```
- Open eye: EAR ≈ 5.0
- Closed eye: EAR ≈ 2.0
- Threshold: EAR > 3.8 indicates blink

**Example:**
```python
gaze.refresh(frame)
if gaze.is_blinking():
    print("Eyes closed!")
    # Pause video, trigger action, etc.
```

**Use Cases:**
- Blink-to-select interfaces
- Fatigue detection (frequent blinking)
- Attention monitoring
- Gaming controls

**Notes:**
- Sensitive to partial eye closure
- May trigger false positives if user squints

---

### `annotated_frame()`

```python
gaze.annotated_frame() -> numpy.ndarray
```

**Description:**
Returns a copy of the current frame with pupils highlighted by green circles.

**Returns:**
- `numpy.ndarray`: BGR image with pupil annotations
- Returns original frame if pupils not located

**Annotation Details:**
- Pupil circles drawn in green `(0, 255, 0)`
- Circle radius adapts to detected pupil size
- Default radius: 5 pixels if detection uncertain

**Example:**
```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    # Get annotated frame for display
    annotated = gaze.annotated_frame()
    cv2.imshow("Gaze Tracking", annotated)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break
```

**Use Cases:**
- Visual debugging
- Demo applications
- Real-time feedback to users
- Recording tracking sessions

**Performance:**
- Creates frame copy (minimal overhead)
- Safe to modify returned frame

---

## Usage Examples

### Basic Tracking Loop

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.pupils_located:
        h_ratio = gaze.horizontal_ratio()
        v_ratio = gaze.vertical_ratio()
        print(f"Gaze: H={h_ratio:.2f}, V={v_ratio:.2f}")

    cv2.imshow("Demo", gaze.annotated_frame())
    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
```

### Direction-Based Control

```python
gaze.refresh(frame)

if gaze.is_left():
    # Move cursor/character left
    cursor_x -= 10
elif gaze.is_right():
    # Move cursor/character right
    cursor_x += 10
elif gaze.is_center():
    # Confirm/select action
    select_item()
```

### Blink Detection

```python
blink_counter = 0
blink_threshold = 3  # Actions trigger after 3 blinks

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.is_blinking():
        blink_counter += 1
        if blink_counter >= blink_threshold:
            print("Action triggered by blinking!")
            blink_counter = 0
    else:
        blink_counter = 0  # Reset if eyes open
```

### Data Logging

```python
import csv
import time

with open('gaze_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'left_x', 'left_y', 'right_x', 'right_y',
                     'h_ratio', 'v_ratio', 'blinking'])

    while True:
        _, frame = webcam.read()
        gaze.refresh(frame)

        if gaze.pupils_located:
            left = gaze.pupil_left_coords()
            right = gaze.pupil_right_coords()

            writer.writerow([
                time.time(),
                left[0], left[1],
                right[0], right[1],
                gaze.horizontal_ratio(),
                gaze.vertical_ratio(),
                gaze.is_blinking()
            ])
```

### Custom Annotations

```python
frame = gaze.annotated_frame()

# Add gaze direction text
if gaze.is_left():
    cv2.putText(frame, "LEFT", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
elif gaze.is_right():
    cv2.putText(frame, "RIGHT", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Add ratio values
h_ratio = gaze.horizontal_ratio()
if h_ratio:
    cv2.putText(frame, f"H: {h_ratio:.2f}", (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

cv2.imshow("Custom Annotated", frame)
```

---

## Return Value Reference

### Method Return Types Summary

| Method | Return Type | None Possible | Range/Values |
|--------|-------------|---------------|--------------|
| `pupils_located` | `bool` | No | `True` or `False` |
| `pupil_left_coords()` | `Tuple[int, int]` | Yes | `(0-width, 0-height)` |
| `pupil_right_coords()` | `Tuple[int, int]` | Yes | `(0-width, 0-height)` |
| `horizontal_ratio()` | `float` | Yes | `0.0` to `1.0` |
| `vertical_ratio()` | `float` | Yes | `0.0` to `1.0` |
| `is_left()` | `bool` | No | `True` or `False` |
| `is_right()` | `bool` | No | `True` or `False` |
| `is_center()` | `bool` | No | `True` or `False` |
| `is_blinking()` | `bool` | No | `True` or `False` |
| `annotated_frame()` | `numpy.ndarray` | No | BGR image array |

### Handling None Values

Methods that can return `None`:

```python
# Safe approach
gaze.refresh(frame)

# Check before using
left = gaze.pupil_left_coords()
if left is not None:
    x, y = left
    # Use coordinates
else:
    print("Left pupil not detected")

# Or use pupils_located first
if gaze.pupils_located:
    left = gaze.pupil_left_coords()  # Guaranteed non-None
    right = gaze.pupil_right_coords()
    h_ratio = gaze.horizontal_ratio()
```

---

## Error Handling

### Common Issues and Solutions

#### No Face Detected

```python
gaze.refresh(frame)
if not gaze.pupils_located:
    # Possible causes:
    # 1. No face in frame
    # 2. Face too far from camera
    # 3. Poor lighting
    # 4. Extreme head pose (>30°)
    print("Cannot detect face - adjust position or lighting")
```

#### Model File Missing

```python
try:
    gaze = GazeTracking()
except FileNotFoundError as e:
    print("Error: shape_predictor_68_face_landmarks.dat not found")
    print("Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
```

#### Camera Access Failure

```python
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Cannot access webcam")
    print("Check camera permissions or try different camera index")
    exit(1)

_, frame = webcam.read()
if frame is None:
    print("Error: Cannot read frame from webcam")
    exit(1)

gaze.refresh(frame)  # Now safe to process
```

### Robust Implementation Pattern

```python
import cv2
from gaze_tracking import GazeTracking

def safe_gaze_tracking():
    try:
        gaze = GazeTracking()
    except FileNotFoundError:
        print("Model file missing!")
        return

    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Cannot access webcam!")
        return

    frame_count = 0
    no_face_count = 0

    while True:
        ret, frame = webcam.read()
        if not ret:
            print("Failed to read frame")
            break

        gaze.refresh(frame)
        frame_count += 1

        if gaze.pupils_located:
            no_face_count = 0
            # Process gaze data
            print(f"Gaze: {gaze.horizontal_ratio():.2f}")
        else:
            no_face_count += 1
            if no_face_count > 30:  # No face for 1 second at 30 FPS
                print("No face detected for extended period")

        cv2.imshow("Tracking", gaze.annotated_frame())
        if cv2.waitKey(1) == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    safe_gaze_tracking()
```

---

## Performance Considerations

### Optimization Tips

1. **Process Every Nth Frame:**
   ```python
   frame_counter = 0
   while True:
       _, frame = webcam.read()

       if frame_counter % 2 == 0:  # Process every 2nd frame
           gaze.refresh(frame)
       frame_counter += 1
   ```

2. **Reduce Resolution:**
   ```python
   _, frame = webcam.read()
   frame_small = cv2.resize(frame, (320, 240))
   gaze.refresh(frame_small)  # 4x faster processing
   ```

3. **Skip Annotation:**
   ```python
   # Don't call annotated_frame() if not needed
   gaze.refresh(frame)
   h_ratio = gaze.horizontal_ratio()  # Just get data
   ```

---

## Type Annotations (For Type Checking)

```python
from typing import Optional, Tuple
import numpy as np

class GazeTracking:
    def __init__(self) -> None: ...

    @property
    def pupils_located(self) -> bool: ...

    def refresh(self, frame: np.ndarray) -> None: ...

    def pupil_left_coords(self) -> Optional[Tuple[int, int]]: ...

    def pupil_right_coords(self) -> Optional[Tuple[int, int]]: ...

    def horizontal_ratio(self) -> Optional[float]: ...

    def vertical_ratio(self) -> Optional[float]: ...

    def is_left(self) -> bool: ...

    def is_right(self) -> bool: ...

    def is_center(self) -> bool: ...

    def is_blinking(self) -> bool: ...

    def annotated_frame(self) -> np.ndarray: ...
```

---

## Additional Resources

- **Installation Guide**: See [README.md](README.md)
- **Algorithm Details**: See [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md)
- **Technical Documentation**: See [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
- **Examples**: See [EXAMPLES.md](EXAMPLES.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

*Last updated: 2026-01-30*
