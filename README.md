# Gaze Tracking

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![GitHub stars](https://img.shields.io/github/stars/JamesTCameron/GazeTracking.svg?style=social)](https://github.com/JamesTCameron/GazeTracking/stargazers)

This is a Python (2 and 3) library that provides a **webcam-based eye tracking system**. It provides precise measurements of biometric data including pupil positions and vision vectors, in real time.

[![Demo](https://i.imgur.com/WNqgQkO.gif)](https://youtu.be/YEZMk1P0-yw)

> **Note:** This is a fork of [antoinelame/GazeTracking](https://github.com/antoinelame/GazeTracking) with additional improvements and maintenance.

## Installation

Clone this project:

```shell
git clone https://github.com/JamesTCameron/GazeTracking.git
```

### For Pip install
Install these dependencies (NumPy, OpenCV, Dlib):

```shell
pip install -r requirements.txt
```

> The Dlib library has four primary prerequisites: Boost, Boost.Python, CMake and X11/XQuartx. If you doesn't have them, you can [read this article](https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/) to know how to easily install them.


### For Anaconda install
Install these dependencies (NumPy, OpenCV, Dlib):

```shell
conda env create --file environment.yml
#After creating environment, activate it
conda activate GazeTracking
```


### Verify Installation

Run the demo:

```shell
python example.py
```

## Simple Demo

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()

    # Get precise biometric measurements
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    horizontal = gaze.horizontal_ratio()
    vertical = gaze.vertical_ratio()

    cv2.putText(new_frame, f"Left: {left_pupil}", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)
    cv2.putText(new_frame, f"Right: {right_pupil}", (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)
    cv2.imshow("Demo", new_frame)

    if cv2.waitKey(1) == 27:
        break
```

## Documentation

In the following examples, `gaze` refers to an instance of the `GazeTracking` class.

### Refresh the frame

```python
gaze.refresh(frame)
```

Pass the frame to analyze (numpy.ndarray). If you want to work with a video stream, you need to put this instruction in a loop, like the example above.

### Position of the left pupil

```python
gaze.pupil_left_coords()
```

Returns the coordinates (x,y) of the left pupil.

### Position of the right pupil

```python
gaze.pupil_right_coords()
```

Returns the coordinates (x,y) of the right pupil.

### Horizontal direction of the gaze

```python
ratio = gaze.horizontal_ratio()
```

Returns a number between 0.0 and 1.0 that indicates the horizontal direction of the gaze. The extreme right is 0.0, the center is 0.5 and the extreme left is 1.0.

### Vertical direction of the gaze

```python
ratio = gaze.vertical_ratio()
```

Returns a number between 0.0 and 1.0 that indicates the vertical direction of the gaze. The extreme top is 0.0, the center is 0.5 and the extreme bottom is 1.0.

### Webcam frame

```python
frame = gaze.annotated_frame()
```

Returns the main frame with pupils highlighted.

## 📚 Comprehensive Documentation

We've created extensive documentation to help you get started and make the most of GazeTracking:

### Getting Started
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation instructions and troubleshooting for all platforms
- **[FAQ.md](FAQ.md)** - Frequently asked questions and answers
- **[WIKI_HOME.md](WIKI_HOME.md)** - Complete documentation hub

### Developer Resources
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation with all methods, parameters, and examples
- **[EXAMPLES.md](EXAMPLES.md)** - Practical code examples: interactive apps, gaming, accessibility, data collection
- **[ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md)** - Visual algorithm explanations with diagrams and formulas
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Deep technical analysis and research references

### Contributing
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing, development workflow, and improvement roadmap
- **[WIKI.md](WIKI.md)** - Original comprehensive wiki with quick answers

### Quick Links
- [What model does GazeTracking use?](TECHNICAL_DOCUMENTATION.md#algorithms-and-models) - Classical CV + pre-trained Dlib models
- [How accurate is it?](FAQ.md#q-how-accurate-is-gazetracking) - ±5-10° angular error
- [Performance optimization tips](ALGORITHM_GUIDE.md#performance-analysis) - Frame skipping, resolution reduction, ROI tracking
- [Use case examples](EXAMPLES.md) - Gaming, accessibility, data collection, and more

## You want to help?

Your suggestions, bug reports, and pull requests are welcome and appreciated! You can also star ⭐️ the project!

**Ways to contribute:**
- Report bugs or request features via [GitHub Issues](https://github.com/JamesTCameron/GazeTracking/issues)
- Submit pull requests (see [CONTRIBUTING.md](CONTRIBUTING.md))
- Improve documentation
- Share your use cases and examples
- Help answer questions in [GitHub Discussions](https://github.com/JamesTCameron/GazeTracking/discussions)

If the detection of your pupils is not completely optimal, you can send a video sample of you looking in different directions to help improve the algorithm.

## Licensing

This project is released by Antoine Lamé under the terms of the MIT Open Source License. View [LICENSE](LICENSE) for more information.
