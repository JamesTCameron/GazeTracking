# GazeTracking Wiki

Welcome to the comprehensive documentation for GazeTracking! This wiki provides deep technical documentation about the eye tracking algorithms, models, and implementation details.

## 📚 Documentation Index

### Getting Started
- **[README.md](README.md)** - Project overview, installation, and basic usage
- **[Example Code](example.py)** - Working demo implementation

### Deep Technical Documentation
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Complete technical deep dive
  - Architecture overview
  - Core components explained
  - Pipeline details
  - Algorithms and models used
  - Performance analysis
  - Improvement roadmap
  - Research references

- **[ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md)** - Algorithm quick reference
  - Visual pipeline diagrams
  - Step-by-step algorithm breakdowns
  - Mathematical formulas
  - Code examples
  - Troubleshooting guide
  - Performance optimization

## 🎯 Quick Answers

### What kind of model does GazeTracking use?

**TL;DR:** GazeTracking uses **classical computer vision** (not deep learning) for iris/pupil detection. It uses two pre-trained ML models for face processing:

1. **Face Detection:** Dlib's HOG (Histogram of Oriented Gradients) + Linear SVM
2. **Facial Landmarks:** Dlib's 68-point predictor (Ensemble of Regression Trees)
3. **Pupil Detection:** Pure OpenCV image processing (bilateral filtering, thresholding, contour analysis)

### How does the eye tracking work?

**Pipeline:**
```
Webcam Frame
    ↓
Face Detection (HOG + SVM)
    ↓
Facial Landmarks (68 points)
    ↓
Eye Isolation (polygon masking)
    ↓
Calibration (adaptive thresholding)
    ↓
Pupil Detection (image processing)
    ↓
Gaze Direction (geometric ratios)
```

**See:** [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md#visual-pipeline) for detailed diagrams

### How can we improve this design?

**Top Improvements:**
1. **Deep Learning Models** - Replace classical CV with CNNs (Mediapipe, MTCNN)
2. **3D Gaze Estimation** - Calculate actual screen coordinates
3. **Head Pose Compensation** - Support rotated heads (±60°)
4. **Person-Specific Calibration** - 5-point calibration for ±1-2° accuracy
5. **Temporal Smoothing** - Kalman filtering for smoother tracking

**See:** [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md#potential-improvements) for complete roadmap

## 📖 Documentation Structure

### For Beginners
Start here if you're new to eye tracking or this project:
1. Read the [README.md](README.md) for basic usage
2. Run the [example.py](example.py) demo
3. Skim [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md) for visual overview

### For Developers
If you want to understand the codebase:
1. Read [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md) - Quick reference with diagrams
2. Explore the [source code](gaze_tracking/) with newfound understanding
3. Check [troubleshooting](ALGORITHM_GUIDE.md#troubleshooting) for common issues

### For Researchers
If you need deep technical details:
1. Read [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Comprehensive analysis
2. Review [research references](TECHNICAL_DOCUMENTATION.md#research-papers-and-resources)
3. Study [improvement roadmap](TECHNICAL_DOCUMENTATION.md#potential-improvements)

### For Contributors
If you want to improve the project:
1. Understand the [architecture](TECHNICAL_DOCUMENTATION.md#architecture-overview)
2. Review [limitations](TECHNICAL_DOCUMENTATION.md#limitations)
3. Pick from [improvement roadmap](TECHNICAL_DOCUMENTATION.md#implementation-roadmap-for-improvements)
4. Submit a pull request!

## 🔍 Core Concepts Explained

### Computer Vision Pipeline
The system uses **classical computer vision** techniques rather than deep learning for pupil detection. This makes it:
- ✅ Fast (runs on CPU)
- ✅ Lightweight (low memory)
- ✅ Simple (easy to understand)
- ❌ Less accurate (±5-10° vs. ±1-2° for DL)
- ❌ Less robust (lighting, head pose)

**Details:** [TECHNICAL_DOCUMENTATION.md - How Eye Tracking Works](TECHNICAL_DOCUMENTATION.md#how-eye-tracking-works)

### Face Detection (HOG + SVM)
- Scans image at multiple scales
- Extracts HOG features (gradient histograms)
- Classifies face/non-face with Linear SVM
- Fast: ~20-50ms per frame

**Details:** [ALGORITHM_GUIDE.md - Face Detection](ALGORITHM_GUIDE.md#1-face-detection-dlib)

### Facial Landmarks (68-point)
- Pre-trained model: `shape_predictor_68_face_landmarks.dat`
- Algorithm: Ensemble of Regression Trees (ERT)
- Trained on iBUG 300-W dataset
- Returns 68 (x,y) coordinates for facial features

**Details:** [ALGORITHM_GUIDE.md - Facial Landmarks](ALGORITHM_GUIDE.md#2-facial-landmark-detection-dlib)

### Pupil Detection (Image Processing)
1. **Bilateral Filter** - Smooth while preserving edges
2. **Morphological Erosion** - Enhance dark regions (iris)
3. **Binary Threshold** - Separate iris from sclera
4. **Contour Detection** - Find iris boundary
5. **Centroid Calculation** - Compute pupil center

**Details:** [ALGORITHM_GUIDE.md - Pupil Detection](ALGORITHM_GUIDE.md#5-pupil-detection-computer-vision)

### Calibration System
- Runs for first 20 frames
- Tests multiple threshold values (5-100)
- Selects threshold where iris occupies ~48% of eye
- Adapts to individual users and lighting

**Details:** [ALGORITHM_GUIDE.md - Calibration](ALGORITHM_GUIDE.md#4-calibration-system)

### Gaze Direction
- Calculates ratio: `pupil_x / eye_width`
- 0.0 = right, 0.5 = center, 1.0 = left
- Averages both eyes for robustness
- Thresholds: ≤0.35 (right), ≥0.65 (left)

**Details:** [ALGORITHM_GUIDE.md - Gaze Direction](ALGORITHM_GUIDE.md#6-gaze-direction-calculation)

### Blink Detection
- Uses Eye Aspect Ratio (EAR)
- Formula: `eye_width / eye_height`
- Open eye: ~5.0, Closed: ~2.0
- Threshold: >3.8 indicates blink

**Details:** [ALGORITHM_GUIDE.md - Blink Detection](ALGORITHM_GUIDE.md#7-blink-detection)

## 🚀 Performance

### Typical Performance
- **Frame Rate:** 12-25 FPS (40-80ms per frame)
- **CPU Usage:** ~30-50% (single core)
- **Memory:** ~200MB
- **Accuracy:** ±5-10° angular error

### Bottlenecks
1. Face detection (50-60% of processing time)
2. Bilateral filtering (15-20%)
3. Multiple eye processing (2x overhead)

### Optimization Tips
- Process every 2nd frame (2x speedup)
- Reduce resolution (4x speedup at 320x240)
- Track face ROI only (2-3x speedup)

**Details:** [ALGORITHM_GUIDE.md - Performance Analysis](ALGORITHM_GUIDE.md#performance-analysis)

## 🔬 Advanced Topics

### Deep Learning Alternatives
Modern eye tracking systems use CNNs:
- **Mediapipe Iris** - Google's 478-point face mesh + iris tracking
- **MPIIGaze** - Appearance-based gaze estimation
- **iTracker** - Screen gaze from face+eye images

**Comparison:** [ALGORITHM_GUIDE.md - Classical CV vs Deep Learning](ALGORITHM_GUIDE.md#comparison-with-alternatives)

### 3D Gaze Estimation
Current system only provides 2D ratios. For screen coordinates:
1. Add head pose estimation (6DOF)
2. Implement 3D eye model
3. Use pupil-glint tracking (requires IR)
4. Or: Train appearance-based CNN

**Details:** [TECHNICAL_DOCUMENTATION.md - 3D Gaze Estimation](TECHNICAL_DOCUMENTATION.md#2-3d-gaze-estimation)

### Calibration Techniques
- **Current:** Automatic threshold calibration
- **Better:** 5-point or 9-point screen calibration
- **Best:** Person-specific polynomial regression

**Details:** [TECHNICAL_DOCUMENTATION.md - Person-Specific Calibration](TECHNICAL_DOCUMENTATION.md#4-person-specific-calibration)

## 🛠️ Development Guide

### Project Structure
```
GazeTracking/
├── gaze_tracking/
│   ├── __init__.py
│   ├── gaze_tracking.py    # Main controller
│   ├── eye.py              # Eye isolation & processing
│   ├── pupil.py            # Pupil detection
│   ├── calibration.py      # Threshold calibration
│   └── trained_models/
│       └── shape_predictor_68_face_landmarks.dat
├── example.py              # Demo application
├── requirements.txt        # Dependencies
├── README.md              # User documentation
├── WIKI.md                # This file
├── TECHNICAL_DOCUMENTATION.md
└── ALGORITHM_GUIDE.md
```

### Key Files

#### `gaze_tracking.py` (Main Controller)
- `refresh(frame)` - Process new frame
- `horizontal_ratio()` - Gaze direction (0.0-1.0)
- `vertical_ratio()` - Vertical gaze (0.0-1.0)
- `is_left() / is_right() / is_center()` - Direction predicates
- `is_blinking()` - Eye closure detection
- `pupil_left_coords() / pupil_right_coords()` - Absolute positions

#### `eye.py` (Eye Processing)
- `_isolate()` - Extract eye region using landmarks
- `_blinking_ratio()` - Calculate eye aspect ratio
- Uses landmarks 36-41 (left eye), 42-47 (right eye)

#### `pupil.py` (Pupil Detection)
- `image_processing()` - Bilateral filter, erosion, threshold
- `detect_iris()` - Contour detection and centroid
- Pure computer vision (no ML)

#### `calibration.py` (Auto-Calibration)
- `evaluate()` - Test frame with multiple thresholds
- `find_best_threshold()` - Optimize for 48% iris coverage
- Collects 20 frames, averages results

### Dependencies
- **dlib** (19.24.4) - Face detection & landmarks
- **opencv-python** (4.10.0.82) - Image processing
- **numpy** (1.26.4) - Numerical computations

### Adding New Features

**Example: Add smoothing to gaze ratios**
```python
# In gaze_tracking.py
class GazeTracking:
    def __init__(self):
        # ... existing code ...
        self.prev_h_ratio = None
        self.alpha = 0.3  # Smoothing factor

    def horizontal_ratio(self):
        current = # ... calculate ratio ...

        if self.prev_h_ratio is None:
            self.prev_h_ratio = current
        else:
            # Exponential moving average
            current = self.alpha * current + (1 - self.alpha) * self.prev_h_ratio
            self.prev_h_ratio = current

        return current
```

## 📊 Use Cases

### Current Best Uses
- ✅ **Education** - Learn eye tracking concepts
- ✅ **Prototyping** - Quick proof-of-concept
- ✅ **Simple Applications** - Basic gaze control (left/right/center)
- ✅ **Research** - Baseline comparison
- ✅ **Accessibility** - Simple gaze-based input

### Not Recommended For
- ❌ High-accuracy applications (use commercial trackers)
- ❌ Clinical/medical use (not validated)
- ❌ Extreme head poses (>30° rotation)
- ❌ Poor lighting conditions
- ❌ Multi-user scenarios (without modification)

## 🤝 Contributing

### Areas Needing Improvement
1. **Deep learning models** - Replace classical CV
2. **3D gaze estimation** - Screen coordinate mapping
3. **Head pose compensation** - Support rotation
4. **Temporal smoothing** - Kalman filtering
5. **Multi-face support** - Track multiple users
6. **Testing** - Add unit tests
7. **Documentation** - More code comments

**Full Roadmap:** [TECHNICAL_DOCUMENTATION.md - Implementation Roadmap](TECHNICAL_DOCUMENTATION.md#implementation-roadmap-for-improvements)

### How to Contribute
1. Fork the repository
2. Pick an improvement from the roadmap
3. Implement with tests
4. Submit pull request
5. Add documentation

## 📚 Further Reading

### Research Papers
- **Kazemi & Sullivan (2014)** - "One Millisecond Face Alignment with an Ensemble of Regression Trees"
- **Duchowski (2017)** - "Eye Tracking Methodology: Theory and Practice"
- **Hansen & Ji (2010)** - "In the Eye of the Beholder: A Survey of Models for Eyes and Gaze"
- **Zhang et al. (2015)** - "Appearance-Based Gaze Estimation in the Wild" (MPIIGaze)

**Complete List:** [TECHNICAL_DOCUMENTATION.md - Research Papers](TECHNICAL_DOCUMENTATION.md#research-papers-and-resources)

### Related Projects
- **Dlib** - Face detection & landmarks (used in this project)
- **OpenFace** - Facial behavior analysis toolkit
- **Mediapipe** - Google's real-time perception pipeline
- **GazeML** - Deep learning gaze estimation
- **PyGaze** - Eye tracking framework

### Online Resources
- **Dlib Documentation:** http://dlib.net/
- **OpenCV Tutorials:** https://docs.opencv.org/
- **Eye Tracking Research:** https://scholar.google.com/scholar?q=eye+tracking

## ❓ FAQ

### Q: What model is used for eye tracking?
**A:** See [What kind of model does GazeTracking use?](#what-kind-of-model-does-gazetracking-use) above.

### Q: How accurate is it?
**A:** ±5-10° angular accuracy. Commercial trackers achieve ±0.5-1°.

### Q: Can it work with glasses?
**A:** Partially. Reflections can interfere. Matte/anti-reflective coatings help.

### Q: Does it need calibration?
**A:** Automatic calibration (first 20 frames). For better accuracy, implement 5-point calibration.

### Q: Can it track multiple people?
**A:** No (currently tracks only the first detected face). See [Multi-Face Support](TECHNICAL_DOCUMENTATION.md#6-multi-face-support).

### Q: What's the minimum hardware requirement?
**A:** Dual-core CPU, 2GB RAM, 640x480 webcam. See [Hardware Requirements](TECHNICAL_DOCUMENTATION.md#hardware-requirements).

### Q: Can I use it on mobile?
**A:** Not optimized for mobile. See [Mobile Deployment](TECHNICAL_DOCUMENTATION.md#9-mobile-and-embedded-deployment).

### Q: How do I improve accuracy?
**A:** Implement person-specific calibration, head pose compensation, or switch to deep learning models.

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/JamesTCameron/GazeTracking/issues)
- **Discussions:** [GitHub Discussions](https://github.com/JamesTCameron/GazeTracking/discussions)
- **Original Project:** [antoinelame/GazeTracking](https://github.com/antoinelame/GazeTracking)

---

## 📝 Documentation Quick Links

| Document | Description | Best For |
|----------|-------------|----------|
| [README.md](README.md) | Installation & basic usage | New users |
| [WIKI.md](WIKI.md) | Documentation index (this page) | Navigation |
| [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md) | Visual algorithm reference | Developers |
| [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) | Deep technical analysis | Researchers |
| [example.py](example.py) | Working code demo | Learning by example |

---

*Last updated: 2026-01-25*
*Created by: Claude (Anthropic) in response to Issue #4*
