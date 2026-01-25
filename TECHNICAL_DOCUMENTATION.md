# GazeTracking: Technical Documentation

## Overview

GazeTracking is a webcam-based eye tracking system that uses **computer vision techniques** rather than machine learning models. The system employs classical computer vision algorithms for face detection, facial landmark detection, and pupil tracking to determine gaze direction in real-time.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Technical Pipeline](#technical-pipeline)
4. [Algorithms and Models](#algorithms-and-models)
5. [How Eye Tracking Works](#how-eye-tracking-works)
6. [Calibration System](#calibration-system)
7. [Performance Considerations](#performance-considerations)
8. [Potential Improvements](#potential-improvements)
9. [References and Further Reading](#references-and-further-reading)

## Architecture Overview

The system consists of four main components:

```
Input Frame → Face Detection → Facial Landmarks → Eye Isolation → Pupil Detection → Gaze Direction
```

### Key Technologies

- **Dlib**: Face detection and facial landmark prediction
- **OpenCV (cv2)**: Image processing and computer vision operations
- **NumPy**: Numerical computations and array operations

## Core Components

### 1. GazeTracking (`gaze_tracking.py`)

The main controller class that orchestrates the entire tracking process.

**Key Responsibilities:**
- Frame analysis coordination
- Face detection using Dlib's HOG-based detector
- Facial landmark extraction using the 68-point predictor
- Gaze direction calculation
- Pupil coordinate management

**Important Methods:**
- `refresh(frame)`: Processes each new frame
- `horizontal_ratio()`: Returns gaze direction (0.0=right, 0.5=center, 1.0=left)
- `vertical_ratio()`: Returns vertical gaze direction
- `is_blinking()`: Detects eye closure

### 2. Eye (`eye.py`)

Handles individual eye processing and isolation.

**Key Responsibilities:**
- Eye region isolation from the face
- Blinking detection via eye aspect ratio
- Pupil initialization for each eye
- Eye frame cropping and masking

**Technical Details:**
- Uses specific landmark points:
  - Left eye: Points 36-41 (from 68-point model)
  - Right eye: Points 42-47 (from 68-point model)
- Creates a masked region containing only the eye
- Calculates blinking ratio: `width / height` of the eye

### 3. Pupil (`pupil.py`)

Detects the iris and estimates pupil position.

**Key Responsibilities:**
- Iris isolation through image processing
- Pupil center calculation using contour analysis
- Threshold-based binarization

**Image Processing Pipeline:**
1. Bilateral filtering (smoothing while preserving edges)
2. Erosion (morphological operation to enhance dark regions)
3. Binary thresholding (separate iris from sclera)
4. Contour detection and centroid calculation

### 4. Calibration (`calibration.py`)

Automatically calibrates the binarization threshold for optimal pupil detection.

**Key Responsibilities:**
- Dynamic threshold optimization per eye
- Adaptation to different lighting conditions
- User-specific calibration

**Calibration Process:**
- Collects 20 frames per eye during initialization
- Tests multiple threshold values (5 to 100, in steps of 5)
- Selects threshold where iris occupies ~48% of eye region
- Averages the best thresholds across frames

## Technical Pipeline

### Step-by-Step Process

#### 1. Frame Input
```python
gaze.refresh(frame)  # RGB frame from webcam
```

#### 2. Face Detection (gaze_tracking.py:44-45)
- Converts frame to grayscale
- Uses **Dlib's HOG (Histogram of Oriented Gradients) + Linear SVM** face detector
- Returns bounding boxes of detected faces
- Processes only the first detected face

```python
frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = dlib.get_frontal_face_detector()(frame_gray)
```

#### 3. Facial Landmark Detection (gaze_tracking.py:48)
- Uses **Dlib's 68-point facial landmark predictor**
- Pre-trained model: `shape_predictor_68_face_landmarks.dat`
- Trained on the **iBUG 300-W dataset**
- Returns 68 (x,y) coordinates for facial features

```python
landmarks = shape_predictor(frame_gray, faces[0])
```

**Landmark Points Used:**
- Points 36-41: Left eye contour
- Points 42-47: Right eye contour

#### 4. Eye Isolation (eye.py:37-67)
- Extracts eye region using landmark points
- Creates a binary mask to isolate the eye
- Crops the frame to contain only the eye region
- Adds 5-pixel margin for processing buffer

**Masking Process:**
```python
# Create polygon mask from eye landmarks
mask = np.full((height, width), 255, np.uint8)
cv2.fillPoly(mask, [eye_region], (0, 0, 0))
eye = cv2.bitwise_not(black_frame, frame.copy(), mask=mask)
```

#### 5. Pupil Detection (pupil.py:37-54)

**Image Processing Steps:**

a. **Bilateral Filtering** (pupil.py:31)
   - Smooths the image while preserving edges
   - Parameters: diameter=10, sigmaColor=15, sigmaSpace=15
   - Reduces noise without blurring the iris boundary

b. **Erosion** (pupil.py:32)
   - Morphological operation with 3x3 kernel
   - 3 iterations to enhance dark regions (iris/pupil)
   - Makes the pupil more prominent

c. **Binary Thresholding** (pupil.py:33)
   - Separates iris (dark) from sclera (white)
   - Uses calibrated threshold value (dynamic per user)
   - Creates binary image: iris=black, rest=white

d. **Contour Detection** (pupil.py:46-47)
   - Finds all contours in the binary image
   - Sorts by area (largest contours represent iris)

e. **Centroid Calculation** (pupil.py:50-52)
   - Uses the second-largest contour (usually the iris)
   - Calculates center using **image moments**:
     ```python
     cx = M10 / M00
     cy = M01 / M00
     ```
   - This gives the (x,y) coordinates of the pupil center

#### 6. Gaze Direction Calculation (gaze_tracking.py:79-97)

**Horizontal Ratio:**
```python
ratio = pupil_x / (eye_center_x * 2 - 10)
```
- 0.0 = Looking right
- 0.5 = Looking center
- 1.0 = Looking left

**Thresholds:**
- `is_right()`: ratio ≤ 0.35
- `is_left()`: ratio ≥ 0.65
- `is_center()`: between 0.35 and 0.65

**Vertical Ratio:**
```python
ratio = pupil_y / (eye_center_y * 2 - 10)
```
- 0.0 = Looking up
- 0.5 = Looking center
- 1.0 = Looking down

#### 7. Blink Detection (eye.py:69-93)

Uses **Eye Aspect Ratio (EAR)**:
```
EAR = eye_width / eye_height
```

- Normal open eye: EAR ≈ 5.0
- Closed eye: EAR ≈ 2.0
- Threshold for blinking: EAR > 3.8 (gaze_tracking.py:118)

## Algorithms and Models

### 1. Face Detection: HOG + Linear SVM

**Histogram of Oriented Gradients (HOG):**
- Feature descriptor that captures edge and gradient structure
- Divides image into small cells
- Computes histogram of gradient directions in each cell
- Creates a feature vector representing the face pattern

**Linear SVM Classifier:**
- Trained to distinguish faces from non-faces
- Uses the HOG feature vector as input
- Fast and efficient for real-time processing

**Source:** Dlib's `get_frontal_face_detector()`

### 2. Facial Landmark Detection: Ensemble of Regression Trees (ERT)

**Model:** `shape_predictor_68_face_landmarks.dat`

**Algorithm:**
- Cascade of regression trees
- Each tree predicts a refinement to landmark positions
- Iteratively improves landmark accuracy
- Trained on iBUG 300-W dataset (68-point facial landmarks)

**Training Dataset:**
- iBUG 300-W (300 Faces in the Wild)
- Indoor and outdoor images
- Various poses, lighting conditions, and expressions

**Publication:**
- "One Millisecond Face Alignment with an Ensemble of Regression Trees" by V. Kazemi and J. Sullivan (2014)

### 3. Iris Detection: Classical Computer Vision

**No ML Model - Pure Computer Vision:**
- Bilateral filtering (edge-preserving smoothing)
- Morphological erosion (enhance dark regions)
- Adaptive thresholding (separate iris from sclera)
- Contour analysis (find iris boundary)
- Moment calculation (compute centroid)

**Why This Approach?**
- Fast and efficient (no neural network overhead)
- Works well for controlled environments (webcam)
- Low computational requirements
- Good accuracy for gaze direction estimation

## How Eye Tracking Works

### Complete Flow Example

1. **User sits in front of webcam**
2. **System captures frame** (640x480 or higher)
3. **Face detector** finds the face bounding box
4. **Landmark predictor** identifies 68 facial points
5. **Eye isolator** extracts left and right eye regions
6. **Calibration phase** (first 20 frames):
   - Tests different threshold values
   - Finds optimal iris detection threshold
   - Averages across multiple frames
7. **Pupil detector** locates iris center in each eye
8. **Gaze calculator** computes horizontal/vertical ratios
9. **Direction classifier** determines gaze direction (left/right/center)
10. **Blink detector** monitors eye aspect ratio
11. **Results returned** to application

### Real-Time Performance

**Typical Processing Time per Frame:**
- Face detection: ~20-50ms
- Landmark detection: ~5-10ms
- Eye processing: ~5-10ms each eye
- Total: ~40-80ms (12-25 FPS)

**Optimization Opportunities:**
- Process every Nth frame
- Use smaller face detector (faster but less accurate)
- Reduce image resolution
- Use GPU acceleration (OpenCV CUDA)

## Calibration System

### Purpose
Different users have different eye characteristics:
- Iris color (darker = easier to detect)
- Eye shape and size
- Lighting conditions
- Camera quality

### Automatic Calibration Process

**Phase 1: Data Collection (First 20 frames)**
```python
for frame in range(20):
    for threshold in [5, 10, 15, ..., 95]:
        iris_size = calculate_iris_percentage(frame, threshold)
        score = abs(iris_size - 0.48)  # Target: 48% iris coverage
    best_threshold = threshold_with_minimum_score
    thresholds.append(best_threshold)
```

**Phase 2: Threshold Averaging**
```python
final_threshold = mean(thresholds)
```

**Target Metric:**
- Iris should occupy approximately **48%** of the eye region
- This ratio works well across most individuals
- Balances between over-segmentation and under-segmentation

### Why 48%?
- Empirically determined sweet spot
- Accounts for pupil, iris, and partial sclera
- Provides reliable contour detection
- Robust across lighting variations

## Performance Considerations

### Strengths
1. **Fast**: Runs in real-time on modest hardware
2. **No training required**: Pre-trained models included
3. **Lightweight**: Small memory footprint (~100MB model)
4. **Robust**: Works across different users without retraining
5. **Simple**: Easy to understand and modify

### Limitations
1. **Requires frontal face**: Doesn't work well with head rotation >30°
2. **Lighting sensitive**: Poor performance in very dark/bright conditions
3. **Single face**: Only tracks the first detected face
4. **Binary thresholding**: May fail with unusual iris colors
5. **No depth information**: Cannot determine absolute gaze point in 3D space
6. **Calibration needed**: First 20 frames require stable gaze
7. **Accuracy**: ±5-10° angular accuracy (vs. ±0.5-1° for commercial eye trackers)

### Hardware Requirements
- **Minimum**:
  - CPU: Dual-core 2.0 GHz
  - RAM: 2GB
  - Webcam: 640x480 @ 15 FPS
- **Recommended**:
  - CPU: Quad-core 2.5 GHz
  - RAM: 4GB
  - Webcam: 1280x720 @ 30 FPS

## Potential Improvements

### 1. **Upgrade to Deep Learning Models**

**Current Limitation:** Classical CV methods struggle with:
- Extreme head poses
- Poor lighting
- Occlusions (glasses, hair)
- Diverse ethnicities and ages

**Proposed Solution:**
- Replace Dlib's HOG detector with **MTCNN** or **RetinaFace** (deep learning face detectors)
- Use **Mediapipe Face Mesh** (478 landmarks) instead of 68-point model
- Implement **deep learning-based iris segmentation** (U-Net or similar)

**Benefits:**
- Better accuracy across diverse conditions
- More robust to head rotation
- Finer facial landmark resolution

**Challenges:**
- Larger model size (50-200MB)
- Higher computational cost
- Requires GPU for real-time performance

### 2. **3D Gaze Estimation**

**Current Limitation:**
- Only provides 2D ratios (horizontal/vertical)
- No screen-space coordinates
- Cannot determine where user is looking on screen

**Proposed Solution:**
- Implement **pupil-glint tracking** (requires IR illumination)
- Use **appearance-based gaze estimation** (CNN regresses gaze vector)
- Add **geometric gaze estimation** using 3D eye model

**Approaches:**
- **MPIIGaze**: CNN-based gaze estimation from eye images
- **GazeNet**: End-to-end deep learning for gaze prediction
- **iTracker**: Uses full face + eye crops for screen gaze

**Benefits:**
- Actual screen coordinates (x, y)
- Better accuracy (±2-3° vs. current ±5-10°)
- Supports multi-monitor setups

### 3. **Head Pose Estimation**

**Current Limitation:**
- Assumes frontal face
- Performance degrades with head rotation

**Proposed Solution:**
- Add **6DOF head pose estimation** (roll, pitch, yaw + translation)
- Use **PnP (Perspective-n-Point)** algorithm with 3D face model
- Compensate gaze direction based on head pose

**Implementation:**
```python
# Use 3D face model + 2D landmarks
object_points = 3D_FACE_MODEL  # Generic 3D face
image_points = landmarks_2d
_, rotation_vector, translation_vector = cv2.solvePnP(
    object_points, image_points, camera_matrix, dist_coeffs
)
# Use rotation to correct gaze vector
```

**Benefits:**
- Works with head tilted/rotated up to 60°
- More natural user interaction
- Better accuracy in real-world scenarios

### 4. **Person-Specific Calibration**

**Current Limitation:**
- Generic threshold calibration
- No adaptation to individual gaze patterns

**Proposed Solution:**
- Implement **5-point or 9-point calibration** procedure
- Build **user-specific gaze mapping model**
- Support **multiple user profiles**

**Calibration Flow:**
1. Display target points on screen
2. User looks at each point for 2-3 seconds
3. Record pupil positions and head pose
4. Train polynomial regression model: `(pupil_pos, head_pose) → screen_pos`
5. Save user profile for future sessions

**Benefits:**
- Accuracy: ±1-2° (vs. current ±5-10°)
- Personalized to each user
- Accounts for anatomical differences

### 5. **Blink and Saccade Detection**

**Current Features:**
- Basic blink detection (binary: open/closed)

**Proposed Enhancements:**
- Detect **microsaccades** (small involuntary eye movements)
- Track **smooth pursuit** vs. **saccadic movements**
- Measure **blink frequency** and **blink duration**
- Detect **fixations** (stable gaze for analysis)

**Applications:**
- Fatigue detection (increased blink rate)
- Reading analysis (fixation duration)
- Attention monitoring
- Gaming input (blink to select)

### 6. **Multi-Face Support**

**Current Limitation:**
- Only tracks one person

**Proposed Solution:**
- Track all detected faces simultaneously
- Assign unique IDs to each person
- Support multi-user scenarios

**Use Cases:**
- Multiple people viewing same screen
- Classroom attention monitoring
- Group interaction analysis

### 7. **Glasses and Occlusion Handling**

**Current Limitation:**
- Struggles with glasses (reflections)
- Hair/bangs can occlude eyes

**Proposed Solution:**
- Train models on **glasses-specific datasets**
- Implement **reflection removal** preprocessing
- Use **attention mechanisms** to focus on visible eye regions

**Techniques:**
- GAN-based reflection removal
- Infrared imaging (penetrates glasses better)
- Multi-modal fusion (visible + IR cameras)

### 8. **Temporal Smoothing**

**Current Limitation:**
- Frame-by-frame processing (jittery results)

**Proposed Solution:**
- Implement **Kalman filtering** for pupil position
- Use **temporal convolution** for gaze smoothing
- Apply **exponential moving average** to reduce noise

**Benefits:**
- Smoother gaze trajectories
- Reduced jitter and noise
- Better user experience

### 9. **Mobile and Embedded Deployment**

**Proposed Solution:**
- Optimize models for **mobile devices** (TensorFlow Lite, ONNX)
- Port to **embedded systems** (Raspberry Pi, Jetson Nano)
- Support **smartphone front cameras**

**Optimization:**
- Model quantization (INT8)
- Pruning and knowledge distillation
- Hardware acceleration (NPU, VPU)

### 10. **Eye State Classification**

**Beyond Current Features:**
- Detect **drowsiness** (partial eye closure, slow blinks)
- Recognize **eye expressions** (wide-eyed, squinting)
- Measure **pupil dilation** (emotional state, cognitive load)

**Applications:**
- Driver drowsiness detection
- Attention and engagement monitoring
- Medical diagnostics

## Implementation Roadmap for Improvements

### Phase 1: Quick Wins (1-2 weeks)
1. Add temporal smoothing (Kalman filter)
2. Implement head pose estimation
3. Add 5-point calibration option
4. Improve glasses handling (reflection removal)

### Phase 2: Medium Complexity (1-2 months)
1. Replace face detector with MTCNN/RetinaFace
2. Implement 3D gaze estimation
3. Add saccade and fixation detection
4. Support multi-face tracking

### Phase 3: Advanced Features (3-6 months)
1. Deep learning iris segmentation
2. Full 3D eye model with pupil-glint tracking
3. Person-specific learning and adaptation
4. Mobile deployment with TFLite

### Phase 4: Research & Innovation (6+ months)
1. Appearance-based gaze estimation (CNN)
2. Multimodal fusion (visible + IR)
3. VR/AR gaze tracking integration
4. Eye state and cognitive load estimation

## Technical Debt and Code Quality

### Areas for Improvement
1. **Error handling**: Limited exception handling in core methods
2. **Type hints**: Add type annotations for better IDE support
3. **Unit tests**: No test coverage currently
4. **Configuration**: Hardcoded thresholds (0.35, 0.65, 3.8, 48%)
5. **Documentation**: Limited inline comments
6. **Logging**: No debug/info logging for troubleshooting

### Recommended Refactoring
```python
# Current
def horizontal_ratio(self):
    if self.pupils_located:
        pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
        ...

# Improved
def horizontal_ratio(self) -> Optional[float]:
    """Calculate horizontal gaze ratio.

    Returns:
        float: Ratio between 0.0 (right) and 1.0 (left), or None if pupils not found.
    """
    if not self.pupils_located:
        return None

    try:
        pupil_left = self._calculate_pupil_ratio(
            self.eye_left, axis='horizontal'
        )
        pupil_right = self._calculate_pupil_ratio(
            self.eye_right, axis='horizontal'
        )
        return (pupil_left + pupil_right) / 2.0
    except Exception as e:
        logger.error(f"Failed to calculate horizontal ratio: {e}")
        return None
```

## Research Papers and Resources

### Face Detection
- **Dalal & Triggs (2005)**: "Histograms of Oriented Gradients for Human Detection"
- **Dlib**: http://dlib.net/face_detector.py.html

### Facial Landmarks
- **Kazemi & Sullivan (2014)**: "One Millisecond Face Alignment with an Ensemble of Regression Trees"
- **iBUG 300-W Dataset**: https://ibug.doc.ic.ac.uk/resources/300-W/

### Eye Tracking
- **Duchowski (2017)**: "Eye Tracking Methodology: Theory and Practice"
- **Hansen & Ji (2010)**: "In the Eye of the Beholder: A Survey of Models for Eyes and Gaze"

### Deep Learning Alternatives
- **Zhang et al. (2015)**: "Appearance-Based Gaze Estimation in the Wild" (MPIIGaze)
- **Krafka et al. (2016)**: "Eye Tracking for Everyone" (GazeCapture/iTracker)
- **Cheng et al. (2020)**: "Appearance-Based Gaze Estimation With Deep Learning: A Review and Benchmark"

### Open Source Projects
- **Dlib**: http://dlib.net/ (face detection & landmarks)
- **OpenFace**: https://github.com/TadasBaltrusaitis/OpenFace (facial behavior analysis)
- **Mediapipe**: https://google.github.io/mediapipe/ (face mesh, iris tracking)
- **GazeML**: https://github.com/swook/GazeML (deep learning gaze estimation)

## Conclusion

GazeTracking uses a **classical computer vision pipeline** rather than deep learning:

1. **HOG + SVM** for face detection (Dlib)
2. **Ensemble of Regression Trees** for 68-point facial landmarks (Dlib)
3. **Bilateral filtering + thresholding + contour analysis** for iris detection (OpenCV)
4. **Geometric calculations** for gaze direction estimation

This approach is **fast, lightweight, and effective** for controlled webcam environments. However, transitioning to deep learning methods (Mediapipe, MTCNN, appearance-based gaze estimation) would significantly improve:
- Accuracy (±1-2° vs. current ±5-10°)
- Robustness (lighting, head pose, occlusions)
- Functionality (3D gaze, screen coordinates, multi-face)

The next steps depend on your use case:
- **For research/experimentation**: Current system is excellent
- **For production/commercial**: Implement Phase 1-2 improvements
- **For high-accuracy applications**: Consider Phase 3-4 with deep learning

The codebase is clean and modular, making it an excellent foundation for implementing these enhancements.
