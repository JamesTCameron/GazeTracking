# Contributing to GazeTracking

Thank you for your interest in contributing to GazeTracking! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Areas Needing Contribution](#areas-needing-contribution)

## Code of Conduct

This project welcomes contributions from everyone. Please be respectful and constructive in all interactions.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/GazeTracking.git
   cd GazeTracking
   ```
3. **Create a branch** for your contribution:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

When filing a bug report, include:
- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs. actual behavior
- **Environment details**:
  - OS (Windows/macOS/Linux)
  - Python version
  - Library versions (dlib, opencv, numpy)
  - Webcam specifications
- **Screenshots or videos** if applicable
- **Error messages** or logs

**Example:**
```
Title: Face detection fails in low light conditions

Description:
When testing with webcam in room with < 100 lux lighting,
face detection fails consistently.

Steps to reproduce:
1. Run example.py in dimly lit room
2. Observe no face bounding box appears

Expected: Face should be detected
Actual: gaze.pupils_located returns False

Environment:
- Ubuntu 22.04
- Python 3.10
- dlib 19.24.4
- opencv-python 4.10.0.82
- Logitech C920 webcam
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear title** describing the enhancement
- **Provide detailed description** of the proposed functionality
- **Explain why this enhancement would be useful** to users
- **List any alternatives** you've considered
- **Include mockups or examples** if applicable

### Contributing Code

1. **Find or create an issue** describing what you plan to work on
2. **Comment on the issue** to let others know you're working on it
3. **Write your code** following our coding standards
4. **Test your changes** thoroughly
5. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip or conda package manager
- Git
- Webcam for testing

### Installation

#### Using pip:
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/GazeTracking.git
cd GazeTracking

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest black flake8
```

#### Using conda:
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/GazeTracking.git
cd GazeTracking

# Create conda environment
conda env create --file environment.yml
conda activate GazeTracking
```

### Running the Demo

```bash
python example.py
```

If the demo runs successfully, your development environment is ready!

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Grouped and sorted (standard library, third-party, local)

### Code Formatting

We recommend using `black` for code formatting:

```bash
black gaze_tracking/
```

### Type Hints

Add type hints to function signatures for better code clarity:

```python
def horizontal_ratio(self) -> Optional[float]:
    """Calculate horizontal gaze ratio.

    Returns:
        float: Ratio between 0.0 (right) and 1.0 (left), or None if pupils not found.
    """
    if not self.pupils_located:
        return None
    # ... rest of implementation
```

### Documentation

- **Docstrings**: Use Google-style docstrings for all public methods
- **Comments**: Explain "why", not "what" (code should be self-explanatory)
- **Examples**: Include usage examples in docstrings when helpful

**Example:**

```python
def refresh(self, frame: np.ndarray) -> None:
    """Analyzes a new frame and updates gaze tracking data.

    This method processes the input frame through the complete pipeline:
    face detection, landmark extraction, eye isolation, and pupil detection.

    Args:
        frame: BGR image from webcam (numpy array, typically 640x480 or higher)

    Example:
        >>> gaze = GazeTracking()
        >>> webcam = cv2.VideoCapture(0)
        >>> _, frame = webcam.read()
        >>> gaze.refresh(frame)
        >>> print(gaze.horizontal_ratio())
        0.52
    """
    # Implementation...
```

## Testing Guidelines

### Manual Testing

Before submitting, test your changes with:

1. **Different lighting conditions**
2. **Various head poses** (frontal, slight rotation)
3. **With and without glasses**
4. **Different webcam resolutions**

### Unit Tests (Future)

We're working on adding automated tests. When contributing new features:

- Write tests for your code
- Ensure all tests pass before submitting
- Add test cases for edge cases

**Future test structure:**
```python
# tests/test_gaze_tracking.py
import unittest
from gaze_tracking import GazeTracking

class TestGazeTracking(unittest.TestCase):
    def test_initialization(self):
        gaze = GazeTracking()
        self.assertIsNotNone(gaze)

    def test_pupil_detection(self):
        # Test with sample frame
        pass
```

## Pull Request Process

### Before Submitting

1. **Update documentation** if you've changed APIs
2. **Test thoroughly** on your local machine
3. **Run code formatters** (black, flake8)
4. **Update CHANGELOG** (if exists) with your changes
5. **Rebase on latest main** to avoid merge conflicts:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### PR Title Format

Use conventional commits format:

- `feat: Add 3D gaze estimation`
- `fix: Resolve pupil detection failure with glasses`
- `docs: Update API reference`
- `refactor: Simplify calibration logic`
- `perf: Optimize bilateral filtering`
- `test: Add unit tests for Eye class`

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Motivation
Why is this change needed? What problem does it solve?

## Changes
- Change 1
- Change 2
- Change 3

## Testing
How was this tested? Include test environments and results.

## Screenshots (if applicable)
Before/after screenshots or demo videos.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tested on multiple environments
- [ ] No breaking changes (or documented if necessary)
```

### Review Process

1. Maintainers will review your PR within 1-2 weeks
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR
4. Your contribution will be included in the next release!

## Areas Needing Contribution

Here are specific areas where we'd love your help:

### High Priority

1. **Unit Tests** (Issue: #TBD)
   - Add pytest-based test suite
   - Test coverage for all modules
   - Integration tests with sample frames

2. **Deep Learning Integration** (Issue: #TBD)
   - Replace HOG face detector with MTCNN or RetinaFace
   - Add Mediapipe Face Mesh option
   - Implement CNN-based iris segmentation

3. **3D Gaze Estimation** (Issue: #TBD)
   - Add head pose estimation (6DOF)
   - Implement 3D eye model
   - Map gaze to screen coordinates

4. **Performance Optimization** (Issue: #TBD)
   - Add Kalman filtering for smoothing
   - Implement frame skipping option
   - ROI tracking to reduce processing time

### Medium Priority

5. **Person-Specific Calibration** (Issue: #TBD)
   - Implement 5-point or 9-point calibration
   - Save/load user profiles
   - Polynomial regression for gaze mapping

6. **Multi-Face Support** (Issue: #TBD)
   - Track multiple faces simultaneously
   - Assign unique IDs to each person
   - Handle face entering/leaving frame

7. **Glasses Handling** (Issue: #TBD)
   - Reflection removal preprocessing
   - Train on glasses-specific datasets
   - Add IR camera support option

8. **Mobile Deployment** (Issue: #TBD)
   - Optimize for mobile devices
   - TensorFlow Lite / ONNX conversion
   - Android/iOS example apps

### Documentation

9. **Video Tutorials** (Issue: #TBD)
   - Installation walkthrough
   - Usage examples
   - Algorithm explanation videos

10. **Use Case Examples** (Issue: #TBD)
    - Gaming control example
    - Accessibility application
    - Attention monitoring demo
    - Reading analysis tool

### Code Quality

11. **Type Annotations** (Issue: #TBD)
    - Add type hints throughout codebase
    - Run mypy for type checking

12. **Error Handling** (Issue: #TBD)
    - Add comprehensive exception handling
    - Meaningful error messages
    - Graceful degradation

## Development Workflow

### Typical Contribution Flow

```bash
# 1. Sync your fork with upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Create feature branch
git checkout -b feat/add-kalman-filtering

# 3. Make changes and commit
git add gaze_tracking/smoothing.py
git commit -m "feat: Add Kalman filtering for pupil smoothing"

# 4. Push to your fork
git push origin feat/add-kalman-filtering

# 5. Create PR on GitHub
# Go to your fork and click "New Pull Request"
```

### Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(calibration): Add 5-point calibration option

Implements user-facing 5-point calibration that improves
accuracy by mapping pupil positions to screen coordinates.

Closes #42
```

```
fix(pupil): Handle contour detection edge case

Fixes crash when no valid contours found in thresholded image.
Now returns None instead of raising IndexError.

Fixes #38
```

## Questions?

- **General questions**: Create a [GitHub Discussion](https://github.com/JamesTCameron/GazeTracking/discussions)
- **Bug reports**: Create a [GitHub Issue](https://github.com/JamesTCameron/GazeTracking/issues)
- **Feature requests**: Create a [GitHub Issue](https://github.com/JamesTCameron/GazeTracking/issues)

## License

By contributing to GazeTracking, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you for contributing to GazeTracking! Your efforts help make eye tracking technology more accessible to everyone.

---

**Need help getting started?** Check out these beginner-friendly issues labeled `good first issue`!
