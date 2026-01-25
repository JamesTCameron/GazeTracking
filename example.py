"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    horizontal_ratio = gaze.horizontal_ratio()
    vertical_ratio = gaze.vertical_ratio()
    left_diameter = gaze.pupil_left_diameter()
    right_diameter = gaze.pupil_right_diameter()

    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 60), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 95), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Horizontal: " + str(horizontal_ratio), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Vertical:   " + str(vertical_ratio), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    if left_diameter:
        cv2.putText(frame, "Left diameter: {:.2f}px".format(left_diameter), (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    if right_diameter:
        cv2.putText(frame, "Right diameter: {:.2f}px".format(right_diameter), (90, 235), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
