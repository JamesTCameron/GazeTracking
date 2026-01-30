# GazeTracking Examples

Practical code examples demonstrating various use cases for the GazeTracking library.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Interactive Applications](#interactive-applications)
- [Data Collection](#data-collection)
- [Gaming and Entertainment](#gaming-and-entertainment)
- [Accessibility Applications](#accessibility-applications)
- [Advanced Techniques](#advanced-techniques)

---

## Basic Examples

### Example 1: Simple Gaze Direction Detection

Display which direction the user is looking in real-time.

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    # Display direction
    text = ""
    if gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break

webcam.release()
cv2.destroyAllWindows()
```

### Example 2: Continuous Ratio Monitoring

Track exact gaze ratios with visual feedback.

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    if gaze.pupils_located:
        h_ratio = gaze.horizontal_ratio()
        v_ratio = gaze.vertical_ratio()

        # Display ratios
        cv2.putText(frame, f"Horizontal: {h_ratio:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Vertical: {v_ratio:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

        # Draw horizontal gaze indicator
        indicator_x = int(h_ratio * frame.shape[1])
        cv2.circle(frame, (indicator_x, frame.shape[0] - 50), 15, (0, 0, 255), -1)
    else:
        cv2.putText(frame, "No face detected", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Gaze Ratios", frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
```

### Example 3: Blink Counter

Count the number of blinks in a session.

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

blink_counter = 0
was_blinking = False

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    # Detect blink transitions (closed -> open)
    is_blinking = gaze.is_blinking()

    if was_blinking and not is_blinking:
        blink_counter += 1

    was_blinking = is_blinking

    # Display blink count
    cv2.putText(frame, f"Blinks: {blink_counter}", (10, 30),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

    if is_blinking:
        cv2.putText(frame, "BLINKING", (10, 70),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Blink Counter", frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
```

---

## Interactive Applications

### Example 4: Gaze-Controlled Menu

Navigate a simple menu using eye gaze.

```python
import cv2
import numpy as np
from gaze_tracking import GazeTracking

class GazeMenu:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        self.menu_items = ["Play", "Settings", "Quit"]
        self.selected_item = 1  # Center item
        self.selection_time = 0
        self.selection_threshold = 30  # Frames to confirm selection

    def run(self):
        while True:
            _, frame = self.webcam.read()
            self.gaze.refresh(frame)

            # Create display
            display = np.zeros((480, 640, 3), dtype=np.uint8)

            # Update selection based on gaze
            if self.gaze.is_left():
                self.selected_item = 0
                self.selection_time += 1
            elif self.gaze.is_center():
                self.selected_item = 1
                self.selection_time += 1
            elif self.gaze.is_right():
                self.selected_item = 2
                self.selection_time += 1
            else:
                self.selection_time = 0

            # Draw menu items
            item_positions = [100, 320, 540]
            for i, item in enumerate(self.menu_items):
                color = (0, 255, 0) if i == self.selected_item else (255, 255, 255)
                cv2.putText(display, item, (item_positions[i], 240),
                           cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)

                # Draw selection progress bar
                if i == self.selected_item:
                    progress = min(self.selection_time / self.selection_threshold, 1.0)
                    bar_width = int(100 * progress)
                    cv2.rectangle(display, (item_positions[i], 260),
                                 (item_positions[i] + bar_width, 270),
                                 (0, 255, 0), -1)

            # Check for selection
            if self.selection_time >= self.selection_threshold:
                selected = self.menu_items[self.selected_item]
                print(f"Selected: {selected}")

                if selected == "Quit":
                    break

                # Show selection feedback
                cv2.putText(display, f"{selected} activated!", (200, 350),
                           cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Gaze Menu", display)
                cv2.waitKey(1000)  # Show for 1 second

                self.selection_time = 0

            cv2.imshow("Gaze Menu", display)

            if cv2.waitKey(1) == 27:
                break

        self.webcam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    menu = GazeMenu()
    menu.run()
```

### Example 5: Gaze-Controlled Cursor

Move a cursor on screen using eye gaze.

```python
import cv2
import numpy as np
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Create a canvas
canvas = np.zeros((600, 800, 3), dtype=np.uint8)

# Cursor position
cursor_x, cursor_y = 400, 300
cursor_speed = 15

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    canvas.fill(0)  # Clear canvas

    if gaze.pupils_located:
        h_ratio = gaze.horizontal_ratio()
        v_ratio = gaze.vertical_ratio()

        # Update cursor position
        if h_ratio < 0.35:  # Looking right
            cursor_x = min(cursor_x + cursor_speed, 800)
        elif h_ratio > 0.65:  # Looking left
            cursor_x = max(cursor_x - cursor_speed, 0)

        if v_ratio < 0.4:  # Looking up
            cursor_y = max(cursor_y - cursor_speed, 0)
        elif v_ratio > 0.6:  # Looking down
            cursor_y = min(cursor_y + cursor_speed, 600)

    # Draw cursor
    cv2.circle(canvas, (cursor_x, cursor_y), 20, (0, 255, 0), -1)
    cv2.circle(canvas, (cursor_x, cursor_y), 25, (255, 255, 255), 2)

    # Draw crosshair at center for calibration
    cv2.line(canvas, (400, 0), (400, 600), (100, 100, 100), 1)
    cv2.line(canvas, (0, 300), (800, 300), (100, 100, 100), 1)

    cv2.putText(canvas, f"Pos: ({cursor_x}, {cursor_y})", (10, 30),
                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Gaze Cursor", canvas)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
```

---

## Data Collection

### Example 6: Gaze Data Logger

Record gaze data to CSV for analysis.

```python
import cv2
import csv
import time
from gaze_tracking import GazeTracking
from datetime import datetime

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Create log file with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"gaze_log_{timestamp}.csv"

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write header
    writer.writerow(['timestamp', 'frame_number', 'pupils_detected',
                     'left_pupil_x', 'left_pupil_y',
                     'right_pupil_x', 'right_pupil_y',
                     'horizontal_ratio', 'vertical_ratio',
                     'is_left', 'is_right', 'is_center', 'is_blinking'])

    frame_number = 0
    start_time = time.time()

    print(f"Recording to {filename}...")
    print("Press ESC to stop recording")

    while True:
        _, frame = webcam.read()
        gaze.refresh(frame)

        current_time = time.time() - start_time
        frame_number += 1

        # Get pupil coordinates
        left = gaze.pupil_left_coords()
        right = gaze.pupil_right_coords()

        # Write data
        writer.writerow([
            current_time,
            frame_number,
            gaze.pupils_located,
            left[0] if left else None,
            left[1] if left else None,
            right[0] if right else None,
            right[1] if right else None,
            gaze.horizontal_ratio(),
            gaze.vertical_ratio(),
            gaze.is_left(),
            gaze.is_right(),
            gaze.is_center(),
            gaze.is_blinking()
        ])

        # Display recording status
        display_frame = gaze.annotated_frame()
        cv2.putText(display_frame, f"Recording: {current_time:.1f}s", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(display_frame, f"Frames: {frame_number}", (10, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Recording", display_frame)

        if cv2.waitKey(1) == 27:
            break

webcam.release()
cv2.destroyAllWindows()

print(f"Recording saved to {filename}")
print(f"Total frames: {frame_number}")
print(f"Duration: {current_time:.2f} seconds")
```

### Example 7: Heatmap Generator

Generate a gaze heatmap showing where user looked most.

```python
import cv2
import numpy as np
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Get frame dimensions
_, sample_frame = webcam.read()
height, width = sample_frame.shape[:2]

# Create heatmap accumulator
heatmap = np.zeros((height, width), dtype=np.float32)

frame_count = 0
duration = 30  # seconds to record

print(f"Recording gaze heatmap for {duration} seconds...")

while frame_count < duration * 30:  # Assuming 30 FPS
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.pupils_located:
        # Get average pupil position
        left = gaze.pupil_left_coords()
        right = gaze.pupil_right_coords()

        if left and right:
            avg_x = (left[0] + right[0]) // 2
            avg_y = (left[1] + right[1]) // 2

            # Add Gaussian blob to heatmap
            cv2.circle(heatmap, (avg_x, avg_y), 30, 1, -1)

    frame_count += 1

    # Display progress
    display = gaze.annotated_frame()
    progress = (frame_count / (duration * 30)) * 100
    cv2.putText(display, f"Recording: {progress:.0f}%", (10, 30),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Recording Heatmap", display)

    if cv2.waitKey(1) == 27:
        break

# Normalize and apply colormap
heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
heatmap = heatmap.astype(np.uint8)
heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

# Overlay heatmap on last frame
overlay = cv2.addWeighted(frame, 0.5, heatmap_colored, 0.5, 0)

cv2.imshow("Gaze Heatmap", overlay)
cv2.imwrite("gaze_heatmap.png", overlay)
print("Heatmap saved as gaze_heatmap.png")

cv2.waitKey(0)
webcam.release()
cv2.destroyAllWindows()
```

---

## Gaming and Entertainment

### Example 8: Gaze-Controlled Pong Game

Simple Pong game controlled by eye gaze.

```python
import cv2
import numpy as np
from gaze_tracking import GazeTracking

class GazePong:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

        # Game settings
        self.width, self.height = 800, 600
        self.paddle_width, self.paddle_height = 20, 100
        self.ball_size = 15

        # Game state
        self.reset_game()

    def reset_game(self):
        self.paddle_y = self.height // 2
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = 5
        self.ball_dy = 5
        self.score = 0

    def run(self):
        while True:
            _, frame = self.webcam.read()
            self.gaze.refresh(frame)

            # Create game canvas
            canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)

            # Update paddle position based on gaze
            if self.gaze.pupils_located:
                v_ratio = self.gaze.vertical_ratio()
                self.paddle_y = int(v_ratio * self.height)
                self.paddle_y = max(self.paddle_height // 2,
                                   min(self.paddle_y, self.height - self.paddle_height // 2))

            # Update ball position
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy

            # Ball collision with top/bottom
            if self.ball_y <= 0 or self.ball_y >= self.height:
                self.ball_dy *= -1

            # Ball collision with paddle
            if self.ball_x <= self.paddle_width:
                if abs(self.ball_y - self.paddle_y) < self.paddle_height // 2:
                    self.ball_dx *= -1
                    self.score += 1
                else:
                    # Game over
                    print(f"Game Over! Score: {self.score}")
                    self.reset_game()

            # Ball goes off right edge
            if self.ball_x >= self.width:
                self.ball_dx *= -1

            # Draw paddle
            paddle_top = self.paddle_y - self.paddle_height // 2
            paddle_bottom = self.paddle_y + self.paddle_height // 2
            cv2.rectangle(canvas, (0, paddle_top), (self.paddle_width, paddle_bottom),
                         (0, 255, 0), -1)

            # Draw ball
            cv2.circle(canvas, (int(self.ball_x), int(self.ball_y)),
                      self.ball_size, (255, 255, 255), -1)

            # Draw score
            cv2.putText(canvas, f"Score: {self.score}", (10, 30),
                       cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("Gaze Pong", canvas)

            if cv2.waitKey(30) == 27:
                break

        self.webcam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = GazePong()
    game.run()
```

---

## Accessibility Applications

### Example 9: Blink-to-Select Interface

Use blinks to select items on screen.

```python
import cv2
import numpy as np
from gaze_tracking import GazeTracking
import time

class BlinkSelector:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        self.items = ["Email", "Browser", "Music", "Photos"]
        self.selected = 0
        self.blink_detected = False
        self.last_blink_time = 0

    def run(self):
        was_blinking = False

        while True:
            _, frame = self.webcam.read()
            self.gaze.refresh(frame)

            # Create display
            display = np.zeros((480, 640, 3), dtype=np.uint8)

            # Detect blink (transition from open to closed to open)
            is_blinking = self.gaze.is_blinking()
            current_time = time.time()

            if was_blinking and not is_blinking:
                # Blink completed
                if current_time - self.last_blink_time > 0.5:  # Debounce
                    print(f"Selected: {self.items[self.selected]}")
                    self.last_blink_time = current_time

                    # Move to next item
                    self.selected = (self.selected + 1) % len(self.items)

            was_blinking = is_blinking

            # Draw items
            for i, item in enumerate(self.items):
                y_pos = 100 + i * 80
                color = (0, 255, 0) if i == self.selected else (255, 255, 255)

                # Draw selection box
                if i == self.selected:
                    cv2.rectangle(display, (50, y_pos - 30), (590, y_pos + 20),
                                 (0, 255, 0), 2)

                cv2.putText(display, item, (60, y_pos),
                           cv2.FONT_HERSHEY_DUPLEX, 1.5, color, 2)

            # Instructions
            cv2.putText(display, "Blink to select", (180, 450),
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (200, 200, 200), 1)

            cv2.imshow("Blink Selector", display)

            if cv2.waitKey(1) == 27:
                break

        self.webcam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    selector = BlinkSelector()
    selector.run()
```

### Example 10: Reading Aid with Gaze Tracking

Track reading patterns and highlight current line being read.

```python
import cv2
import numpy as np
from gaze_tracking import GazeTracking

class ReadingAid:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        self.text_lines = [
            "Eye tracking can help understand",
            "how people read and process text.",
            "This application highlights the line",
            "you are currently looking at,",
            "making it easier to follow along."
        ]

    def run(self):
        while True:
            _, frame = self.webcam.read()
            self.gaze.refresh(frame)

            # Create text display
            display = np.zeros((600, 800, 3), dtype=np.uint8)

            # Determine which line user is looking at
            current_line = 2  # Default to middle

            if self.gaze.pupils_located:
                v_ratio = self.gaze.vertical_ratio()
                current_line = int(v_ratio * len(self.text_lines))
                current_line = max(0, min(current_line, len(self.text_lines) - 1))

            # Draw text lines
            for i, line in enumerate(self.text_lines):
                y_pos = 150 + i * 60

                # Highlight current line
                if i == current_line:
                    cv2.rectangle(display, (30, y_pos - 35), (770, y_pos + 10),
                                 (50, 50, 0), -1)
                    color = (0, 255, 255)
                    thickness = 2
                else:
                    color = (200, 200, 200)
                    thickness = 1

                cv2.putText(display, line, (40, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)

            # Show instructions
            cv2.putText(display, "Look at a line to highlight it", (200, 550),
                       cv2.FONT_HERSHEY_DUPLEX, 0.7, (150, 150, 150), 1)

            cv2.imshow("Reading Aid", display)

            if cv2.waitKey(1) == 27:
                break

        self.webcam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = ReadingAid()
    app.run()
```

---

## Advanced Techniques

### Example 11: Multi-Zone Gaze Detection

Divide screen into zones and detect which zone user is looking at.

```python
import cv2
import numpy as np
from gaze_tracking import GazeTracking

class ZoneDetector:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

        # Define 3x3 grid of zones
        self.zones = []
        for row in range(3):
            for col in range(3):
                self.zones.append({
                    'row': row,
                    'col': col,
                    'name': f"Zone {row * 3 + col + 1}"
                })

    def get_current_zone(self):
        if not self.gaze.pupils_located:
            return None

        h_ratio = self.gaze.horizontal_ratio()
        v_ratio = self.gaze.vertical_ratio()

        # Map ratios to 3x3 grid
        col = 2 if h_ratio < 0.35 else (0 if h_ratio > 0.65 else 1)
        row = 0 if v_ratio < 0.35 else (2 if v_ratio > 0.65 else 1)

        zone_index = row * 3 + col
        return self.zones[zone_index]

    def run(self):
        while True:
            _, frame = self.webcam.read()
            self.gaze.refresh(frame)

            # Create display
            display = np.zeros((600, 800, 3), dtype=np.uint8)

            current_zone = self.get_current_zone()

            # Draw 3x3 grid
            for zone in self.zones:
                x1 = zone['col'] * 266 + 10
                y1 = zone['row'] * 200 + 10
                x2 = x1 + 256
                y2 = y1 + 190

                # Highlight active zone
                if current_zone and zone == current_zone:
                    color = (0, 255, 0)
                    thickness = 5
                else:
                    color = (100, 100, 100)
                    thickness = 2

                cv2.rectangle(display, (x1, y1), (x2, y2), color, thickness)

                # Draw zone name
                text_x = x1 + 70
                text_y = y1 + 100
                cv2.putText(display, zone['name'], (text_x, text_y),
                           cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow("Zone Detector", display)

            if cv2.waitKey(1) == 27:
                break

        self.webcam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = ZoneDetector()
    detector.run()
```

### Example 12: Gaze Smoothing with Moving Average

Reduce jitter by applying temporal smoothing.

```python
import cv2
from collections import deque
from gaze_tracking import GazeTracking

class SmoothedGazeTracker:
    def __init__(self, smoothing_window=5):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

        # Buffers for smoothing
        self.h_ratios = deque(maxlen=smoothing_window)
        self.v_ratios = deque(maxlen=smoothing_window)

    def get_smoothed_ratios(self):
        if len(self.h_ratios) == 0:
            return None, None

        h_smooth = sum(self.h_ratios) / len(self.h_ratios)
        v_smooth = sum(self.v_ratios) / len(self.v_ratios)

        return h_smooth, v_smooth

    def run(self):
        while True:
            _, frame = self.webcam.read()
            self.gaze.refresh(frame)

            if self.gaze.pupils_located:
                h_ratio = self.gaze.horizontal_ratio()
                v_ratio = self.gaze.vertical_ratio()

                # Add to buffers
                self.h_ratios.append(h_ratio)
                self.v_ratios.append(v_ratio)

            # Get smoothed values
            h_smooth, v_smooth = self.get_smoothed_ratios()

            # Display
            display = self.gaze.annotated_frame()

            if h_smooth is not None:
                # Raw values
                cv2.putText(display, f"Raw H: {self.gaze.horizontal_ratio():.2f}", (10, 30),
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                cv2.putText(display, f"Raw V: {self.gaze.vertical_ratio():.2f}", (10, 60),
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

                # Smoothed values
                cv2.putText(display, f"Smooth H: {h_smooth:.2f}", (10, 100),
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(display, f"Smooth V: {v_smooth:.2f}", (10, 130),
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Smoothed Gaze", display)

            if cv2.waitKey(1) == 27:
                break

        self.webcam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = SmoothedGazeTracker(smoothing_window=10)
    tracker.run()
```

---

## Tips and Best Practices

1. **Always check `pupils_located` before accessing gaze data**
2. **Use try-except blocks for robust error handling**
3. **Implement smoothing for more stable tracking**
4. **Calibrate thresholds for your specific use case**
5. **Provide visual feedback to users**
6. **Test in various lighting conditions**
7. **Consider frame rate vs. accuracy tradeoffs**

## Additional Resources

- **API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
- **Technical Details**: [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
- **Algorithm Guide**: [ALGORITHM_GUIDE.md](ALGORITHM_GUIDE.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

*Last updated: 2026-01-30*
