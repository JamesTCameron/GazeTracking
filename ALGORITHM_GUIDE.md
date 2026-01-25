# GazeTracking Algorithm Guide

## Quick Reference

### What Model Does GazeTracking Use?

**Short Answer:** GazeTracking does **NOT** use a machine learning model for iris/pupil detection. It uses **classical computer vision** techniques (filtering, thresholding, contours).

**ML Models Used:**
1. **Face Detection**: Dlib's HOG (Histogram of Oriented Gradients) + Linear SVM
2. **Facial Landmarks**: Dlib's 68-point predictor (Ensemble of Regression Trees)

**No ML Used:**
- Iris/pupil detection (pure OpenCV image processing)
- Gaze direction calculation (geometric ratios)
- Blink detection (aspect ratio calculation)

---

## Visual Pipeline

```
┌─────────────────┐
│   Webcam Frame  │
│   (RGB Image)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Convert to Gray │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   Face Detection (Dlib)     │
│   HOG + SVM Classifier      │
│   Returns: Bounding box     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Facial Landmarks (Dlib)     │
│ 68-point predictor          │
│ Returns: 68 (x,y) points    │
└────────┬────────────────────┘
         │
         ├──────────────────┬──────────────────┐
         ▼                  ▼                  ▼
    ┌────────┐         ┌────────┐      ┌──────────┐
    │ Left   │         │ Right  │      │ Blinking │
    │ Eye    │         │ Eye    │      │ Ratio    │
    └───┬────┘         └───┬────┘      └──────────┘
        │                  │
        ▼                  ▼
   ┌─────────────────────────────┐
   │   Eye Isolation             │
   │   - Polygon mask            │
   │   - Crop eye region         │
   └────────┬────────────────────┘
            │
            ▼
   ┌─────────────────────────────┐
   │   Calibration (first 20)    │
   │   - Test thresholds         │
   │   - Find optimal value      │
   └────────┬────────────────────┘
            │
            ▼
   ┌─────────────────────────────┐
   │   Pupil Detection           │
   │   1. Bilateral filter       │
   │   2. Morphological erosion  │
   │   3. Binary threshold       │
   │   4. Find contours          │
   │   5. Calculate centroid     │
   └────────┬────────────────────┘
            │
            ▼
   ┌─────────────────────────────┐
   │   Gaze Direction            │
   │   - Horizontal ratio        │
   │   - Vertical ratio          │
   │   - Is left/right/center?   │
   └─────────────────────────────┘
```

---

## Detailed Algorithm Breakdown

### 1. Face Detection (Dlib)

**Algorithm:** Histogram of Oriented Gradients (HOG) + Linear SVM

**How it works:**

```
Input: Grayscale image
│
├─ Step 1: Divide image into 8x8 pixel cells
│
├─ Step 2: For each cell:
│    ├─ Calculate gradient magnitude and direction
│    └─ Create histogram of gradient directions (9 bins)
│
├─ Step 3: Normalize histograms in overlapping blocks
│
├─ Step 4: Concatenate all histograms → HOG feature vector
│
└─ Step 5: Feed to Linear SVM classifier
     ├─ Trained on positive examples (faces)
     ├─ Trained on negative examples (non-faces)
     └─ Output: Face or not face (+ confidence)
```

**Sliding Window:**
- Detector scans image at multiple scales
- Applies classifier at each position
- Returns bounding boxes where faces detected

**Performance:**
- Fast: ~20-50ms per frame
- Robust to frontal faces
- Struggles with profile views (>45° rotation)

---

### 2. Facial Landmark Detection (Dlib)

**Algorithm:** Ensemble of Regression Trees (ERT)

**Model:** `shape_predictor_68_face_landmarks.dat`

**How it works:**

```
Input: Face bounding box + grayscale image
│
├─ Step 1: Initialize landmarks at mean shape
│
├─ Step 2: Extract features around each landmark
│    └─ Pixel intensity differences in local regions
│
├─ Step 3: For each tree in ensemble (cascade):
│    ├─ Predict displacement for each landmark
│    ├─ Update landmark positions
│    └─ Refine estimate
│
├─ Step 4: Repeat for N trees (typically 10-15)
│
└─ Output: 68 (x, y) coordinates
```

**68 Landmark Points:**
```
0-16:  Jawline
17-21: Left eyebrow
22-26: Right eyebrow
27-35: Nose
36-41: Left eye (used for tracking)
42-47: Right eye (used for tracking)
48-67: Mouth
```

**Eye Landmarks:**
```
Left eye:                Right eye:
    37──38                  43──44
   /      \                /      \
  36      39              42      45
   \      /                \      /
    41──40                  47──46
```

**Training:**
- Dataset: iBUG 300-W (300 Faces In-The-Wild)
- 3,837 images with manual annotations
- Covers variations in pose, expression, lighting

**Performance:**
- Fast: ~5-10ms per face
- Accurate: ±3-5 pixel error on average
- Trained offline (no retraining needed)

---

### 3. Eye Isolation

**Goal:** Extract only the eye region from the face

**Steps:**

```python
# 1. Get eye landmark points
left_eye_points = [36, 37, 38, 39, 40, 41]
eye_polygon = [(landmarks[i].x, landmarks[i].y) for i in left_eye_points]

# 2. Create binary mask
mask = np.full(frame.shape, 255, dtype=np.uint8)
cv2.fillPoly(mask, [eye_polygon], (0, 0, 0))

# 3. Apply mask to isolate eye
eye_isolated = cv2.bitwise_not(black_frame, frame, mask=mask)

# 4. Crop to bounding box
min_x = min(point[0] for point in eye_polygon) - 5  # 5px margin
max_x = max(point[0] for point in eye_polygon) + 5
min_y = min(point[1] for point in eye_polygon) - 5
max_y = max(point[1] for point in eye_polygon) + 5
eye_cropped = eye_isolated[min_y:max_y, min_x:max_x]
```

**Visual:**
```
Original Frame        Mask                Eye Isolated
┌─────────────┐      ┌─────────────┐     ┌─────────────┐
│             │      │█████████████│     │             │
│   ┌─────┐   │      │█┌───────┐█│     │   ┌─────┐   │
│   │ eye │   │  →   │█│       │█│  →  │   │ eye │   │
│   └─────┘   │      │█└───────┘█│     │   └─────┘   │
│             │      │█████████████│     │             │
└─────────────┘      └─────────────┘     └─────────────┘
                    (white = masked)
```

---

### 4. Calibration System

**Goal:** Find optimal threshold for iris detection

**Problem:**
- Different iris colors (blue vs. brown)
- Different lighting conditions
- Different camera sensors

**Solution:** Adaptive calibration per user

**Algorithm:**

```
For each of first 20 frames:
    For threshold in [5, 10, 15, 20, ..., 95]:
        1. Apply threshold to eye image
        2. Calculate iris percentage:
           iris_percentage = black_pixels / total_pixels
        3. Score = |iris_percentage - 0.48|

    best_threshold[frame] = threshold with minimum score

final_threshold = average(best_threshold)
```

**Why 48%?**
- Empirical sweet spot
- Too low → includes too much white (sclera)
- Too high → excludes parts of iris
- 48% works across most eye types

**Visual Example:**

```
Threshold = 30 (too low)    Threshold = 60 (good)      Threshold = 90 (too high)
┌──────────────┐            ┌──────────────┐          ┌──────────────┐
│              │            │              │          │              │
│  ████████    │            │   ███████    │          │    ████      │
│  ████████    │            │   ███████    │          │    ████      │
│  ████████    │            │   ███████    │          │    ████      │
│              │            │              │          │              │
└──────────────┘            └──────────────┘          └──────────────┘
  70% black (too much)       48% black (perfect)       20% black (too little)
```

---

### 5. Pupil Detection (Computer Vision)

**No machine learning - pure image processing!**

#### Step 5.1: Bilateral Filtering

**Purpose:** Smooth noise while preserving edges

**Formula:**
```
BF(x) = Σ w(i,j,k,l) * I(k,l)
where w considers both:
  - Spatial distance: ||(i,j) - (k,l)||
  - Intensity difference: |I(i,j) - I(k,l)|
```

**Parameters:**
- Diameter: 10 pixels
- Sigma color: 15
- Sigma space: 15

**Effect:**
```
Before                  After
┌──────────────┐       ┌──────────────┐
│ ░░░░░░░░░░░░ │       │              │
│ ░░████████░░ │       │   ████████   │
│ ░░████████░░ │   →   │   ████████   │
│ ░░████████░░ │       │   ████████   │
│ ░░░░░░░░░░░░ │       │              │
└──────────────┘       └──────────────┘
(noisy)                (smooth edges)
```

#### Step 5.2: Morphological Erosion

**Purpose:** Enhance dark regions (iris/pupil)

**Operation:**
```
kernel = [[1, 1, 1],
          [1, 1, 1],
          [1, 1, 1]]  # 3x3

Output(x,y) = min(Input(x+i, y+j)) for all i,j in kernel
```

**Iterations:** 3

**Effect:**
```
Before (1 iteration)    After (3 iterations)
┌──────────────┐       ┌──────────────┐
│              │       │              │
│   ████████   │       │    ██████    │
│   ████████   │   →   │    ██████    │
│   ████████   │       │    ██████    │
│              │       │              │
└──────────────┘       └──────────────┘
(lighter iris)         (darker, more prominent)
```

#### Step 5.3: Binary Thresholding

**Purpose:** Separate iris (dark) from sclera (white)

**Formula:**
```
Output(x,y) = 0   if Input(x,y) < threshold
              255 if Input(x,y) ≥ threshold
```

**Threshold:** Calibrated value (typically 50-70)

**Effect:**
```
Grayscale               Binary
┌──────────────┐       ┌──────────────┐
│     ░░░░     │       │              │
│   ░░████░░   │       │              │
│   ░█████░░   │   →   │   ████████   │
│   ░░████░░   │       │   ████████   │
│     ░░░░     │       │              │
└──────────────┘       └──────────────┘
(gradients)            (binary: iris=black)
```

#### Step 5.4: Contour Detection

**Purpose:** Find boundaries of iris

**Algorithm:** Border following (OpenCV)

```
1. Scan image left-to-right, top-to-bottom
2. When black pixel found after white:
   → Start contour tracing
3. Follow boundary clockwise
4. Store contour points
5. Repeat until all contours found
```

**Sorting:**
```python
contours = sorted(contours, key=cv2.contourArea)
# contours[-1] = largest (usually white area)
# contours[-2] = second largest (usually iris)
```

**Why second-largest?**
- Largest contour = background/sclera
- Second-largest = iris
- Smaller contours = noise/reflections

#### Step 5.5: Centroid Calculation

**Purpose:** Find center of iris

**Formula (Image Moments):**
```
M00 = ΣΣ I(x,y)           # Total mass
M10 = ΣΣ x * I(x,y)       # First moment in x
M01 = ΣΣ y * I(x,y)       # First moment in y

centroid_x = M10 / M00
centroid_y = M01 / M00
```

**Visual:**
```
Binary iris contour     Centroid calculation
┌──────────────┐       ┌──────────────┐
│              │       │              │
│   ████████   │       │   ████████   │
│   ████████   │   →   │   ███★███   │  ← Center
│   ████████   │       │   ████████   │
│              │       │              │
└──────────────┘       └──────────────┘
```

**Robustness:**
- Works for irregular shapes
- Handles partial occlusions
- Fast computation (no iterations)

---

### 6. Gaze Direction Calculation

**Input:** Pupil (x, y) coordinates

**Output:** Gaze direction ratio

#### Horizontal Ratio

**Formula:**
```python
ratio = pupil_x / (eye_center_x * 2 - 10)

# Average both eyes:
horizontal_ratio = (left_ratio + right_ratio) / 2
```

**Interpretation:**
```
0.0 ← Looking RIGHT
│
├─ 0.1
├─ 0.2
├─ 0.3
├─ 0.35 ← Threshold: is_right() returns True
├─ 0.4
├─ 0.5 ← CENTER
├─ 0.6
├─ 0.65 ← Threshold: is_left() returns True
├─ 0.7
├─ 0.8
├─ 0.9
│
1.0 ← Looking LEFT
```

**Visual:**
```
Looking Right        Looking Center       Looking Left
┌────────────┐      ┌────────────┐      ┌────────────┐
│ ┌────────┐ │      │ ┌────────┐ │      │ ┌────────┐ │
│ │ ●      │ │      │ │   ●    │ │      │ │      ● │ │
│ └────────┘ │      │ └────────┘ │      │ └────────┘ │
└────────────┘      └────────────┘      └────────────┘
ratio ≤ 0.35        0.35 < ratio < 0.65  ratio ≥ 0.65
```

#### Vertical Ratio

**Formula:**
```python
ratio = pupil_y / (eye_center_y * 2 - 10)

# Average both eyes:
vertical_ratio = (left_ratio + right_ratio) / 2
```

**Interpretation:**
```
0.0 ← Looking UP
│
├─ 0.2
├─ 0.4
├─ 0.5 ← CENTER
├─ 0.6
├─ 0.8
│
1.0 ← Looking DOWN
```

#### Why "* 2 - 10"?

**Explanation:**
```
eye_center_x = width / 2 = 30 (example)
width = eye_center_x * 2 = 60

Normalization:
pupil_x / 60 gives ratio in [0, 1]

The "-10" is a magic number (empirical adjustment):
- Accounts for margin around eye
- Improves ratio distribution
- Makes thresholds more intuitive
```

**Better approach (for future improvement):**
```python
# Calculate relative position within eye bounds
eye_width = max_x - min_x
eye_height = max_y - min_y

ratio_x = (pupil_x - min_x) / eye_width
ratio_y = (pupil_y - min_y) / eye_height
```

---

### 7. Blink Detection

**Algorithm:** Eye Aspect Ratio (EAR)

**Formula:**
```
EAR = eye_width / eye_height

where:
  eye_width = distance(left_corner, right_corner)
  eye_height = average(
    distance(top_mid, bottom_mid),
    distance(top_mid2, bottom_mid2)
  )
```

**Visual:**
```
Open eye (EAR ≈ 5.0):
  37──38
 /      \
36      39
 \      /
  41──40

Closed eye (EAR ≈ 2.0):
36─37─38─39
```

**Threshold:**
```python
is_blinking = (left_EAR + right_EAR) / 2 > 3.8
```

**Why 3.8?**
- Open eye: EAR ≈ 5.0
- Closed eye: EAR ≈ 2.0
- Threshold 3.8 = midpoint with buffer
- Prevents false positives from partial closure

**Robustness:**
- Works across different eye shapes
- Independent of face size
- Fast computation (no image processing)

---

## Performance Analysis

### Computational Complexity

| Component | Algorithm | Time Complexity | Typical Time |
|-----------|-----------|-----------------|--------------|
| Face Detection | HOG + SVM | O(n * m * s) | 20-50ms |
| Facial Landmarks | ERT | O(t * p * f) | 5-10ms |
| Eye Isolation | Masking | O(w * h) | 1-2ms |
| Bilateral Filter | Convolution | O(w * h * k²) | 3-5ms |
| Erosion | Morphology | O(w * h * k² * i) | 2-3ms |
| Thresholding | Pixel-wise | O(w * h) | <1ms |
| Contour Detection | Border following | O(w * h) | 1-2ms |
| Centroid | Moments | O(n) | <1ms |
| **Total** | | | **40-80ms** |

**Legend:**
- n, m = image dimensions
- s = number of scales
- t = number of trees
- p = number of landmarks
- f = feature evaluations
- w, h = eye region size
- k = kernel size
- i = iterations
- n = contour points

### Bottlenecks

1. **Face Detection** (50-60% of time)
   - Solution: Use faster detector (MTCNN, RetinaFace)
   - Alternative: Process every 2nd/3rd frame

2. **Bilateral Filtering** (15-20% of time)
   - Solution: Use Gaussian blur (faster, less quality)
   - Alternative: Reduce filter diameter

3. **Multiple Eye Processing** (2x overhead)
   - Solution: Parallelize left/right eye processing
   - Alternative: Track only one eye (less accurate)

### Optimization Strategies

#### 1. Frame Skipping
```python
frame_counter = 0
if frame_counter % 2 == 0:  # Process every 2nd frame
    gaze.refresh(frame)
frame_counter += 1
```
- Speedup: 2x
- Accuracy loss: Minimal (interpolate between frames)

#### 2. Resolution Reduction
```python
frame_small = cv2.resize(frame, (320, 240))
gaze.refresh(frame_small)
```
- Speedup: 4x (640x480 → 320x240)
- Accuracy loss: ~5-10%

#### 3. ROI Tracking
```python
# After first detection, track only face region
if face_detected:
    face_roi = frame[y:y+h, x:x+w]
    gaze.refresh(face_roi)
```
- Speedup: 2-3x
- Requires: Face tracking (Kalman filter)

---

## Comparison with Alternatives

### Classical CV vs. Deep Learning

| Aspect | GazeTracking (Classical) | Deep Learning (e.g., Mediapipe) |
|--------|--------------------------|----------------------------------|
| **Model Type** | HOG+SVM, ERT, Thresholding | CNN, U-Net, ResNet |
| **Training** | Pre-trained (Dlib) | Pre-trained (Google) |
| **Accuracy** | ±5-10° | ±1-3° |
| **Speed** | 40-80ms (CPU) | 10-30ms (GPU), 50-100ms (CPU) |
| **Model Size** | 100MB | 10-50MB (quantized) |
| **Memory** | ~200MB | ~500MB-2GB |
| **Lighting** | Sensitive | More robust |
| **Head Pose** | Frontal only (<30°) | Up to 60° rotation |
| **Glasses** | Struggles (reflections) | Better (learned) |
| **3D Gaze** | No | Yes (some models) |
| **Dependencies** | Dlib, OpenCV | TensorFlow/PyTorch |

### When to Use Each

**Use GazeTracking (Classical):**
- ✅ Controlled environment (webcam, indoor)
- ✅ Frontal face
- ✅ CPU-only deployment
- ✅ Simple requirements (left/right/center)
- ✅ Learning/prototyping
- ✅ Embedded systems (Raspberry Pi)

**Use Deep Learning:**
- ✅ Unconstrained environment
- ✅ Variable head poses
- ✅ GPU available
- ✅ High accuracy needed (±1-2°)
- ✅ 3D gaze estimation
- ✅ Commercial applications

---

## Code Examples

### Example 1: Basic Usage
```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    # Get gaze direction
    if gaze.is_left():
        print("Looking left")
    elif gaze.is_right():
        print("Looking right")
    elif gaze.is_center():
        print("Looking center")

    # Get exact ratios
    h_ratio = gaze.horizontal_ratio()  # 0.0 - 1.0
    v_ratio = gaze.vertical_ratio()    # 0.0 - 1.0
    print(f"Horizontal: {h_ratio:.2f}, Vertical: {v_ratio:.2f}")
```

### Example 2: Pupil Coordinates
```python
# Get absolute pupil positions
left_pupil = gaze.pupil_left_coords()   # (x, y)
right_pupil = gaze.pupil_right_coords() # (x, y)

if left_pupil:
    print(f"Left pupil at: {left_pupil}")
if right_pupil:
    print(f"Right pupil at: {right_pupil}")
```

### Example 3: Blink Detection
```python
if gaze.is_blinking():
    print("User is blinking or eyes closed")
    # Trigger action (pause video, etc.)
```

### Example 4: Annotated Output
```python
# Get frame with pupils highlighted
annotated = gaze.annotated_frame()
cv2.imshow("Gaze Tracking", annotated)
```

### Example 5: Logging Gaze Data
```python
import time
import csv

with open('gaze_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'h_ratio', 'v_ratio', 'blinking'])

    while True:
        _, frame = webcam.read()
        gaze.refresh(frame)

        if gaze.pupils_located:
            writer.writerow([
                time.time(),
                gaze.horizontal_ratio(),
                gaze.vertical_ratio(),
                gaze.is_blinking()
            ])
```

---

## Troubleshooting

### Issue 1: Face Not Detected

**Symptoms:**
- `gaze.pupils_located` returns False
- No pupil coordinates

**Solutions:**
1. Check lighting (ensure face is well-lit)
2. Position face closer to camera
3. Ensure frontal face orientation
4. Check camera resolution (minimum 640x480)

### Issue 2: Pupil Detection Fails

**Symptoms:**
- Face detected but no pupil tracking
- Erratic pupil positions

**Solutions:**
1. **Recalibrate:** Restart program (first 20 frames)
2. **Check lighting:** Avoid strong backlighting
3. **Remove glasses:** Reflections interfere
4. **Clean camera:** Smudges affect quality

### Issue 3: Inaccurate Gaze Direction

**Symptoms:**
- Reports "left" when looking center
- Thresholds don't match expectations

**Solutions:**
1. **Adjust thresholds:**
   ```python
   # In gaze_tracking.py, modify:
   def is_right(self):
       return self.horizontal_ratio() <= 0.40  # was 0.35

   def is_left(self):
       return self.horizontal_ratio() >= 0.60  # was 0.65
   ```

2. **Personalized calibration:** Track user-specific ratios

### Issue 4: Performance Issues

**Symptoms:**
- Low FPS (< 10)
- Lag in tracking

**Solutions:**
1. Reduce resolution: `frame = cv2.resize(frame, (320, 240))`
2. Process every Nth frame: `if frame_count % 2 == 0: gaze.refresh(frame)`
3. Use faster face detector (future improvement)

### Issue 5: Glasses Interference

**Symptoms:**
- Reflections cause false detections
- Pupil jumps around

**Solutions:**
1. **Adjust lighting:** Avoid overhead lights
2. **Matte glasses:** Use anti-reflective coating
3. **IR camera:** Infrared penetrates glasses better (hardware change)

---

## Summary

### Key Takeaways

1. **Not a "model-based" eye tracker:** Uses classical CV, not deep learning for pupil detection
2. **Two ML models:** Face detection (HOG+SVM) and landmarks (ERT), both pre-trained
3. **Image processing pipeline:** Filtering → Thresholding → Contours → Centroids
4. **Fast and lightweight:** Runs real-time on CPU
5. **Limitations:** Frontal face, controlled lighting, moderate accuracy
6. **Best for:** Prototyping, education, simple applications

### Next Steps to Improve

**Short-term (weeks):**
- Add Kalman filtering for smoother tracking
- Implement 5-point calibration
- Support multiple users

**Medium-term (months):**
- Replace with MTCNN/RetinaFace for face detection
- Add 3D gaze estimation
- Implement head pose compensation

**Long-term (6+ months):**
- Deep learning iris segmentation
- Appearance-based gaze estimation
- VR/AR integration

---

## Additional Resources

- **GazeTracking Repository:** [github.com/JamesTCameron/GazeTracking](https://github.com/JamesTCameron/GazeTracking)
- **Dlib Documentation:** [dlib.net](http://dlib.net/)
- **OpenCV Tutorials:** [docs.opencv.org](https://docs.opencv.org/)
- **Eye Tracking Papers:** See TECHNICAL_DOCUMENTATION.md

---

*Last updated: 2026-01-25*
