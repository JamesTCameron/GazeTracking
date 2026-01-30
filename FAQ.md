# Frequently Asked Questions (FAQ)

Common questions and answers about GazeTracking.

## Table of Contents

- [General Questions](#general-questions)
- [Installation and Setup](#installation-and-setup)
- [Technical Questions](#technical-questions)
- [Troubleshooting](#troubleshooting)
- [Performance and Accuracy](#performance-and-accuracy)
- [Use Cases and Applications](#use-cases-and-applications)
- [Development and Contributing](#development-and-contributing)

---

## General Questions

### Q: What is GazeTracking?

**A:** GazeTracking is a Python library that provides webcam-based eye tracking. It detects your pupils and determines where you're looking in real-time using computer vision techniques.

### Q: What kind of model does GazeTracking use?

**A:** GazeTracking uses **classical computer vision** (not deep learning) for pupil detection:
- **Face Detection**: Dlib's HOG (Histogram of Oriented Gradients) + Linear SVM
- **Facial Landmarks**: Dlib's 68-point predictor (Ensemble of Regression Trees)
- **Pupil Detection**: Pure OpenCV image processing (filtering, thresholding, contours)

See [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) for details.

### Q: Is GazeTracking free to use?

**A:** Yes! GazeTracking is open source under the MIT License. You can use it freely for personal, educational, research, and commercial projects.

### Q: Do I need special hardware?

**A:** No. GazeTracking works with any standard webcam. Recommended specifications:
- Resolution: 640x480 or higher
- Frame rate: 15 FPS or higher
- Any USB webcam or built-in laptop camera

### Q: Does it work offline?

**A:** Yes! Once installed, GazeTracking works completely offline. No internet connection required.

---

## Installation and Setup

### Q: What are the system requirements?

**A:**
- **OS**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **CPU**: Dual-core 2.0 GHz (minimum), Quad-core 2.5 GHz (recommended)
- **RAM**: 2GB (minimum), 4GB (recommended)
- **Webcam**: 640x480 @ 15 FPS (minimum)

### Q: How do I install GazeTracking?

**A:**
```bash
# Clone the repository
git clone https://github.com/JamesTCameron/GazeTracking.git
cd GazeTracking

# Install dependencies
pip install -r requirements.txt

# Run the demo
python example.py
```

See [README.md](README.md) for detailed instructions.

### Q: Installation fails with "Could not find dlib". What should I do?

**A:** Dlib has prerequisites (Boost, CMake, etc.). Solutions:

**On Ubuntu/Debian:**
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

**On macOS:**
```bash
brew install cmake
pip install dlib
```

**On Windows:**
- Use pre-built wheels: `pip install dlib-binary`
- Or follow: https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/

### Q: Where do I get the `shape_predictor_68_face_landmarks.dat` file?

**A:** It's included in the repository under `gaze_tracking/trained_models/`. If missing:
1. Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
2. Extract the `.dat` file
3. Place it in `gaze_tracking/trained_models/`

### Q: Can I use conda instead of pip?

**A:** Yes!
```bash
conda env create --file environment.yml
conda activate GazeTracking
python example.py
```

---

## Technical Questions

### Q: How accurate is GazeTracking?

**A:** Typical accuracy is **±5-10° angular error**. This is sufficient for:
- ✅ Directional controls (left/right/center)
- ✅ Zone-based interactions (which screen area)
- ✅ Attention monitoring
- ❌ Precise screen coordinate tracking (use commercial trackers: ±0.5-1°)

### Q: What frame rate can I expect?

**A:** Typical performance:
- **Frame rate**: 12-25 FPS (40-80ms per frame)
- **CPU usage**: 30-50% (single core)
- **Memory**: ~200MB

Factors affecting speed:
- Image resolution (higher = slower)
- CPU speed
- Number of faces in frame

### Q: Can it track multiple people simultaneously?

**A:** No, currently it tracks only the first detected face. Multi-face support is a potential future enhancement. See [TECHNICAL_DOCUMENTATION.md - Multi-Face Support](TECHNICAL_DOCUMENTATION.md#6-multi-face-support).

### Q: Does it work with glasses?

**A:** **Partially.** Challenges:
- Reflections can interfere with pupil detection
- Works better with matte/anti-reflective coatings
- Thick frames may occlude eyes

**Tips:**
- Adjust lighting to minimize reflections
- Position light sources to the side, not overhead
- Try tilting head slightly

### Q: Can it work in the dark?

**A:** No. The system requires sufficient lighting to detect pupils. Minimum recommended: ~100 lux (typical indoor lighting).

**Solutions for low light:**
- Add desk lamp near monitor
- Use webcam with good low-light performance
- Consider infrared camera (requires code modifications)

### Q: How does the calibration work?

**A:** Automatic calibration runs during the **first 20 frames**:
1. Tests multiple threshold values (5-100)
2. Selects threshold where iris occupies ~48% of eye region
3. Averages results across 20 frames
4. Adapts to your eye color and lighting

**Tips:**
- Look straight ahead during first 2 seconds
- Ensure good lighting
- Keep head still during calibration

See [ALGORITHM_GUIDE.md - Calibration](ALGORITHM_GUIDE.md#4-calibration-system).

### Q: Can I manually adjust the calibration?

**A:** Yes, you can modify thresholds in the code:

```python
# In gaze_tracking.py
def is_right(self):
    return self.horizontal_ratio() <= 0.40  # Adjust from 0.35

def is_left(self):
    return self.horizontal_ratio() >= 0.60  # Adjust from 0.65
```

### Q: Does it provide 3D gaze estimation?

**A:** No. Currently provides only 2D ratios (horizontal/vertical). 3D gaze estimation (screen coordinates) is a planned enhancement. See [TECHNICAL_DOCUMENTATION.md - 3D Gaze Estimation](TECHNICAL_DOCUMENTATION.md#2-3d-gaze-estimation).

---

## Troubleshooting

### Q: "No face detected" - What's wrong?

**A:** Common causes and solutions:

1. **Poor lighting**
   - Solution: Add more light, ensure face is well-lit

2. **Face too far/close**
   - Solution: Position 50-80 cm from camera

3. **Extreme head angle** (>30° rotation)
   - Solution: Face camera more directly

4. **Camera resolution too low**
   - Solution: Check camera settings, use 640x480 minimum

5. **Multiple monitors** (using wrong camera)
   - Solution: Try different camera index: `cv2.VideoCapture(1)`

### Q: Pupils are detected but gaze direction is wrong

**A:** Solutions:

1. **Recalibrate**: Restart the program and look straight ahead during first 2 seconds

2. **Adjust thresholds**: Modify `is_left()` / `is_right()` thresholds in code

3. **Check lighting**: Ensure even lighting on face (no strong shadows)

4. **Clean camera**: Smudges affect quality

### Q: Tracking is jittery/unstable

**A:** Solutions:

1. **Add smoothing**: Use moving average (see [EXAMPLES.md - Example 12](EXAMPLES.md#example-12-gaze-smoothing-with-moving-average))

2. **Improve lighting**: Consistent lighting reduces noise

3. **Process fewer frames**: Only process every 2nd frame

4. **Stabilize head**: Use chin rest or headrest

### Q: High CPU usage - How can I optimize?

**A:** Optimization strategies:

1. **Reduce resolution**:
   ```python
   frame_small = cv2.resize(frame, (320, 240))
   gaze.refresh(frame_small)
   ```

2. **Skip frames**:
   ```python
   if frame_counter % 2 == 0:  # Process every 2nd frame
       gaze.refresh(frame)
   ```

3. **ROI tracking**: Only process face region after first detection

See [ALGORITHM_GUIDE.md - Performance Analysis](ALGORITHM_GUIDE.md#performance-analysis).

### Q: Works on my laptop but not desktop - Why?

**A:** Likely webcam differences:
- Different cameras have different quality
- Try adjusting lighting
- Check camera specifications
- External webcams often work better than built-in ones

### Q: Error: "shape_predictor_68_face_landmarks.dat not found"

**A:** The model file is missing or in wrong location:
1. Check `gaze_tracking/trained_models/` folder exists
2. Download model: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
3. Extract and place in `trained_models/` folder

---

## Performance and Accuracy

### Q: How can I improve accuracy?

**A:** Best practices:

1. **Good lighting**: Even illumination on face
2. **Stable head position**: Minimize head movement
3. **Frontal face**: Face camera directly
4. **Clean camera**: Remove smudges
5. **Proper distance**: 50-80 cm from camera
6. **Remove distractions**: No strong backlighting
7. **Calibrate**: Let automatic calibration complete

Advanced improvements:
- Implement person-specific calibration
- Add head pose compensation
- Use smoothing algorithms

### Q: Why is vertical tracking less accurate than horizontal?

**A:** Eyelids partially occlude pupils when looking up/down, making vertical detection harder. This is a limitation of 2D image-based tracking.

**Solutions:**
- Use larger vertical thresholds (e.g., <0.4 for up, >0.6 for down)
- Focus on horizontal tracking for critical applications
- Implement 3D gaze estimation for better vertical accuracy

### Q: Can I make it work at different distances from camera?

**A:** Yes, but accuracy varies:
- **Optimal**: 50-80 cm
- **Acceptable**: 40-100 cm
- **Poor**: <40 cm or >100 cm

The system automatically adapts to face size, but extreme distances reduce pupil detection accuracy.

### Q: How do I benchmark performance on my system?

**A:** Add timing code:

```python
import time

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

times = []

for _ in range(100):
    _, frame = webcam.read()

    start = time.time()
    gaze.refresh(frame)
    end = time.time()

    times.append(end - start)

print(f"Average processing time: {sum(times)/len(times)*1000:.2f}ms")
print(f"Estimated FPS: {1/(sum(times)/len(times)):.1f}")
```

---

## Use Cases and Applications

### Q: What can I build with GazeTracking?

**A:** Example applications:

**Accessibility:**
- Gaze-controlled mouse/keyboard
- Assistive communication devices
- Hands-free computer control

**Gaming:**
- Gaze-based game controls
- Eye-tracking enabled games
- Virtual reality enhancements

**Research:**
- Reading pattern analysis
- Attention monitoring
- User experience studies
- Cognitive load measurement

**Health:**
- Fatigue detection (blink frequency)
- Focus/concentration monitoring
- Therapy progress tracking

See [EXAMPLES.md](EXAMPLES.md) for code examples.

### Q: Can I use it for user authentication?

**A:** Not recommended for security-critical authentication:
- Pupil positions alone are not unique biometric identifiers
- Easily spoofed with photographs
- Accuracy not sufficient for reliable authentication

Better uses: convenience features, preference detection, attention verification.

### Q: Is it suitable for driver monitoring?

**A:** For research/prototypes: Yes
For production systems: No

Limitations:
- Not validated for safety-critical applications
- Requires controlled environment (cabin lighting)
- Head pose variations affect accuracy

Commercial driver monitoring systems use:
- Infrared cameras
- Deep learning models
- Redundant sensors
- Safety certifications

### Q: Can it be used in VR/AR applications?

**A:** Current version is not optimized for VR/AR, which requires:
- Very high accuracy (±1°)
- High frame rate (90+ FPS)
- Head-mounted cameras
- 3D gaze vectors

Consider alternatives:
- Tobii eye tracking SDKs
- Pupil Labs
- Commercial VR eye tracking solutions

---

## Development and Contributing

### Q: How can I contribute to the project?

**A:** Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas needing help:**
- Deep learning model integration
- 3D gaze estimation
- Performance optimization
- Unit tests
- Documentation
- Bug fixes

### Q: Can I modify the code for my project?

**A:** Yes! MIT License allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

Requirements:
- Include original license and copyright notice
- See [LICENSE](LICENSE) for details

### Q: How do I add new features?

**A:**
1. Fork the repository
2. Create feature branch: `git checkout -b feat/my-feature`
3. Make changes and test
4. Submit pull request

See [CONTRIBUTING.md - Development Workflow](CONTRIBUTING.md#development-workflow).

### Q: Where can I report bugs?

**A:** Create a GitHub issue: https://github.com/JamesTCameron/GazeTracking/issues

Include:
- Clear description of the bug
- Steps to reproduce
- Environment details (OS, Python version, hardware)
- Error messages or logs
- Screenshots/videos if applicable

### Q: Is there a roadmap for future features?

**A:** Yes! See [TECHNICAL_DOCUMENTATION.md - Implementation Roadmap](TECHNICAL_DOCUMENTATION.md#implementation-roadmap-for-improvements).

**High priority:**
- Deep learning models (MTCNN, Mediapipe)
- 3D gaze estimation
- Head pose compensation
- Kalman filtering for smoothing
- Person-specific calibration

### Q: Can I use this in my research paper?

**A:** Yes! Please cite:

```
@software{gazetracking2026,
  author = {Cameron, James T. and Lamé, Antoine},
  title = {GazeTracking: Webcam-based Eye Tracking Library},
  year = {2026},
  url = {https://github.com/JamesTCameron/GazeTracking}
}
```

---

## Platform-Specific Questions

### Q: Does it work on Raspberry Pi?

**A:** Yes, but with reduced performance:
- Recommended: Raspberry Pi 4 (4GB+ RAM)
- Expected FPS: 5-10 (vs. 15-25 on desktop)
- Use lower resolution for better performance
- Consider optimization techniques (frame skipping, ROI tracking)

### Q: Can I run it on Android/iOS?

**A:** Not directly. Would require:
- Porting to mobile platform
- Optimizing for mobile CPUs
- Adapting for front-facing cameras
- Mobile-specific UI

Consider:
- Google ML Kit for mobile
- Mediapipe (has mobile support)
- Or use GazeTracking as reference for mobile implementation

### Q: Does it work on macOS with Apple Silicon (M1/M2)?

**A:** Yes, with some considerations:
- Use conda for easier dependency management
- dlib may require special build steps
- OpenCV works natively on Apple Silicon
- Performance is excellent on M1/M2 chips

---

## Support and Community

### Q: Where can I get help?

**A:** Multiple options:

1. **Documentation**:
   - [README.md](README.md) - Getting started
   - [API_REFERENCE.md](API_REFERENCE.md) - Complete API docs
   - [EXAMPLES.md](EXAMPLES.md) - Code examples
   - [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Deep dive

2. **GitHub**:
   - Issues: Bug reports and feature requests
   - Discussions: Questions and community help

3. **Original Project**:
   - https://github.com/antoinelame/GazeTracking

### Q: Is there commercial support available?

**A:** This is an open-source project without official commercial support. For production applications requiring support, consider:
- Hiring developers with computer vision expertise
- Commercial eye tracking solutions (Tobii, Pupil Labs)
- Consulting services

### Q: Can I hire someone to implement features?

**A:** Yes! Options:
- Post on GitHub Discussions to find contributors
- Hire freelance developers with CV experience
- Contact maintainers for recommendations

---

## Comparison with Alternatives

### Q: How does this compare to commercial eye trackers?

**A:**

| Feature | GazeTracking | Commercial (e.g., Tobii) |
|---------|-------------|-------------------------|
| **Cost** | Free | $100-$10,000+ |
| **Accuracy** | ±5-10° | ±0.5-1° |
| **Hardware** | Any webcam | Specialized hardware |
| **Setup** | Instant | Calibration required |
| **Portability** | High | Low (fixed setup) |
| **Use Case** | Prototyping, research | Production, clinical |

**Use GazeTracking for**: Learning, prototyping, non-critical applications
**Use commercial for**: High-accuracy needs, medical, safety-critical

### Q: Should I use deep learning models instead?

**A:** Depends on requirements:

**Use GazeTracking (classical CV) if:**
- CPU-only deployment
- Low memory footprint needed
- Simple directional controls sufficient
- Learning computer vision concepts

**Use deep learning if:**
- GPU available
- Higher accuracy needed (±1-3°)
- Complex head poses
- Production application

See [ALGORITHM_GUIDE.md - Comparison](ALGORITHM_GUIDE.md#comparison-with-alternatives).

### Q: What about Mediapipe Iris?

**A:** Mediapipe offers:
- Better accuracy (±2-3°)
- More robust (lighting, poses)
- 478-point face mesh
- Google-backed support

But:
- Larger model size
- Requires TensorFlow
- More complex integration

GazeTracking is simpler for learning and prototyping.

---

## Legal and Privacy

### Q: Does GazeTracking collect any data?

**A:** No. GazeTracking:
- Runs completely locally
- Does not send data anywhere
- Does not save images/videos (unless you code it to)
- Does not track users

### Q: Are there privacy concerns with eye tracking?

**A:** General eye tracking considerations:
- Webcam access required (users should be informed)
- Gaze patterns can reveal attention and interest
- If deploying publicly, follow privacy regulations (GDPR, CCPA)
- Obtain user consent before tracking

### Q: Can I use this in commercial applications?

**A:** Yes, MIT License permits commercial use. However:
- Include original license and copyright
- Test thoroughly for your specific use case
- Consider accuracy limitations
- Follow applicable privacy laws

---

## Still Have Questions?

- **Open an issue**: https://github.com/JamesTCameron/GazeTracking/issues
- **Start a discussion**: https://github.com/JamesTCameron/GazeTracking/discussions
- **Check the docs**: See links below

## Additional Resources

- [README.md](README.md) - Installation and quick start
- [API_REFERENCE.md](API_REFERENCE.md) - Complete API documentation
- [EXAMPLES.md](EXAMPLES.md) - Practical code examples
- [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md) - Algorithm explanations
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Technical deep dive
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

*Last updated: 2026-01-30*
