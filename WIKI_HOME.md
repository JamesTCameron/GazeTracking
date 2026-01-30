# GazeTracking Wiki Home

Welcome to the comprehensive GazeTracking documentation! This page serves as your starting point for understanding and using the GazeTracking library.

## 📚 Quick Navigation

### Getting Started
- **[README](README.md)** - Installation and quick start guide
- **[Setup Guide](SETUP_GUIDE.md)** - Detailed installation and troubleshooting
- **[FAQ](FAQ.md)** - Frequently asked questions

### Documentation
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Examples](EXAMPLES.md)** - Practical code examples and use cases
- **[Algorithm Guide](ALGORITHM_GUIDE.md)** - Visual algorithm explanations
- **[Technical Documentation](TECHNICAL_DOCUMENTATION.md)** - Deep technical analysis

### Contributing
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[License](LICENSE)** - MIT License details

---

## 🎯 Quick Start

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.is_left():
        print("Looking left")
    elif gaze.is_right():
        print("Looking right")
    elif gaze.is_center():
        print("Looking center")

    cv2.imshow("Demo", gaze.annotated_frame())

    if cv2.waitKey(1) == 27:
        break
```

---

## 📖 Documentation Structure

### For Beginners
Start here if you're new to eye tracking or this project:

1. **[README.md](README.md)** - Get started with installation and basic usage
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions for your platform
3. **[EXAMPLES.md](EXAMPLES.md)** - See practical code examples
4. **[FAQ.md](FAQ.md)** - Find answers to common questions

### For Developers
If you want to understand the codebase and build applications:

1. **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation with all methods
2. **[ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md)** - Visual pipeline and algorithm explanations
3. **[EXAMPLES.md](EXAMPLES.md)** - Interactive applications, gaming, accessibility examples
4. **[Source Code](gaze_tracking/)** - Explore the implementation

### For Researchers
If you need deep technical details or want to extend the system:

1. **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Comprehensive technical analysis
2. **[ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md)** - Algorithm formulas and performance analysis
3. **Research References** - See citations in technical documentation
4. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Improvement roadmap and contribution areas

### For Contributors
If you want to improve the project:

1. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and workflow
2. **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Architecture and improvement roadmap
3. **GitHub Issues** - Browse open issues and feature requests
4. **GitHub Discussions** - Participate in community discussions

---

## 🔍 What is GazeTracking?

GazeTracking is a Python library that provides **webcam-based eye tracking**. It detects your pupils and determines where you're looking in real-time using computer vision techniques.

### Key Features

✅ **Easy to use** - Simple API, works with any webcam
✅ **Fast** - Real-time tracking at 12-25 FPS on CPU
✅ **Lightweight** - No GPU required, ~200MB memory
✅ **Open source** - MIT License, free for any use
✅ **Cross-platform** - Windows, macOS, Linux

### What Can You Build?

**Accessibility Applications:**
- Gaze-controlled mouse/keyboard
- Assistive communication devices
- Hands-free computer control

**Gaming & Entertainment:**
- Gaze-based game controls
- Interactive experiences
- Virtual reality enhancements

**Research & Analysis:**
- Reading pattern analysis
- Attention monitoring
- User experience studies
- Cognitive load measurement

**Health & Wellness:**
- Fatigue detection
- Focus monitoring
- Therapy progress tracking

See **[EXAMPLES.md](EXAMPLES.md)** for complete code examples.

---

## 🚀 Technology Overview

### How Does It Work?

GazeTracking uses **classical computer vision** (not deep learning) for real-time eye tracking:

1. **Face Detection** - Dlib's HOG + SVM detector finds your face
2. **Facial Landmarks** - 68-point model locates eyes and facial features
3. **Eye Isolation** - Extracts eye regions using polygon masking
4. **Calibration** - Automatically adapts to your eyes (first 20 frames)
5. **Pupil Detection** - Image processing (filtering, thresholding, contours) finds pupils
6. **Gaze Direction** - Geometric calculations determine where you're looking

**See:** [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md) for detailed visual explanations

### Performance

- **Frame Rate**: 12-25 FPS (40-80ms per frame)
- **Accuracy**: ±5-10° angular error
- **CPU Usage**: ~30-50% (single core)
- **Memory**: ~200MB

### Models Used

1. **Face Detection**: HOG (Histogram of Oriented Gradients) + Linear SVM
2. **Facial Landmarks**: Ensemble of Regression Trees (68-point predictor)
3. **Pupil Detection**: Pure OpenCV (no ML - just image processing)

**See:** [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) for deep technical analysis

---

## 📊 Common Use Cases

### Direction Detection

```python
if gaze.is_left():
    # User looking left
elif gaze.is_right():
    # User looking right
elif gaze.is_center():
    # User looking center
```

### Continuous Tracking

```python
h_ratio = gaze.horizontal_ratio()  # 0.0 (right) to 1.0 (left)
v_ratio = gaze.vertical_ratio()    # 0.0 (up) to 1.0 (down)
```

### Pupil Coordinates

```python
left = gaze.pupil_left_coords()    # (x, y) in pixels
right = gaze.pupil_right_coords()  # (x, y) in pixels
```

### Blink Detection

```python
if gaze.is_blinking():
    # Eyes are closed
```

**See:** [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation

---

## 🛠️ Installation

### Quick Install (pip)

```bash
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking
pip install -r requirements.txt
python example.py
```

### Using Conda

```bash
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking
conda env create --file environment.yml
conda activate GazeTracking
python example.py
```

**See:** [SETUP_GUIDE.md](SETUP_GUIDE.md) for platform-specific instructions and troubleshooting

---

## ❓ Frequently Asked Questions

### Does it work with glasses?
Partially. Reflections can interfere. Works better with anti-reflective coatings.

### Can it track multiple people?
No, currently tracks only the first detected face.

### What's the accuracy?
±5-10° angular error (sufficient for directional controls, not precise screen coordinates).

### Does it need calibration?
Automatic calibration runs during first 20 frames. No manual calibration required.

### Can I use it commercially?
Yes! MIT License permits commercial use.

**See:** [FAQ.md](FAQ.md) for complete FAQ

---

## 📚 Documentation Index

| Document | Description | Best For |
|----------|-------------|----------|
| [README.md](README.md) | Quick start guide | New users |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Installation & troubleshooting | Setup help |
| [API_REFERENCE.md](API_REFERENCE.md) | Complete API docs | Developers |
| [EXAMPLES.md](EXAMPLES.md) | Code examples | Learning by example |
| [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md) | Algorithm explanations | Understanding how it works |
| [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) | Technical deep dive | Researchers |
| [FAQ.md](FAQ.md) | Common questions | Quick answers |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guide | Contributors |
| [WIKI.md](WIKI.md) | Original wiki | Alternative navigation |

---

## 🤝 Contributing

Contributions are welcome! Areas needing help:

- **Deep Learning Integration** - Replace classical CV with CNNs
- **3D Gaze Estimation** - Calculate screen coordinates
- **Performance Optimization** - Add Kalman filtering, frame skipping
- **Multi-Face Support** - Track multiple people
- **Testing** - Add unit tests
- **Documentation** - Improve code comments

**See:** [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

---

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/JamesTCameron/GazeTracking/issues) - Bug reports and feature requests
- **Discussions**: [GitHub Discussions](https://github.com/JamesTCameron/GazeTracking/discussions) - Questions and community help
- **Original Project**: [antoinelame/GazeTracking](https://github.com/antoinelame/GazeTracking) - Original implementation

---

## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🌟 Credits

- **Original Author**: Antoine Lamé
- **Maintainer**: James T. Cameron
- **Contributors**: See GitHub contributors list

---

*Last updated: 2026-01-30*
