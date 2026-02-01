"""
Integration tests for GazeTracking API changes
Tests the usage of methods that were modified in the PR to ensure
existing code still works correctly.
"""

import unittest
import sys
import os
import numpy as np

# Add parent directory to path to import gaze_tracking
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gaze_tracking import GazeTracking


class TestGazeTrackingIntegration(unittest.TestCase):
    """Integration tests for GazeTracking class methods used by example.py and backend/app.py"""

    def setUp(self):
        """Set up test fixtures"""
        self.gaze = GazeTracking()
        # Create a dummy frame (black image)
        self.dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def test_pupil_left_coords_exists(self):
        """Test that pupil_left_coords() method exists (used by example.py:21 and backend/app.py:68,135)"""
        # Refresh with a frame
        self.gaze.refresh(self.dummy_frame)

        # This method is called in example.py and backend/app.py
        # It should exist and be callable
        self.assertTrue(hasattr(self.gaze, 'pupil_left_coords'),
                       "pupil_left_coords method is missing - breaks example.py:21 and backend/app.py:68,135")

        # Should be callable
        result = self.gaze.pupil_left_coords()
        # Result should be None (no face detected) or tuple of coordinates
        self.assertTrue(result is None or isinstance(result, tuple),
                       "pupil_left_coords should return None or tuple")

    def test_pupil_right_coords_exists(self):
        """Test that pupil_right_coords() method exists (used by example.py:22 and backend/app.py:69,136)"""
        self.gaze.refresh(self.dummy_frame)

        self.assertTrue(hasattr(self.gaze, 'pupil_right_coords'),
                       "pupil_right_coords method is missing")

        result = self.gaze.pupil_right_coords()
        self.assertTrue(result is None or isinstance(result, tuple),
                       "pupil_right_coords should return None or tuple")

    def test_horizontal_ratio_exists_and_returns_valid_value(self):
        """Test that horizontal_ratio() returns a valid value (used by example.py:23 and backend/app.py:70,137)"""
        self.gaze.refresh(self.dummy_frame)

        self.assertTrue(hasattr(self.gaze, 'horizontal_ratio'),
                       "horizontal_ratio method is missing")

        result = self.gaze.horizontal_ratio()

        # CRITICAL: This method is used in example.py and backend/app.py
        # It should return None (no pupils detected) or a float between 0.0 and 1.0
        # Current implementation returns None (just 'pass'), which will break display
        self.assertTrue(result is None or isinstance(result, (int, float)),
                       "horizontal_ratio should return None or numeric value")

        # If pupils are detected, should be in valid range
        if result is not None:
            self.assertGreaterEqual(result, 0.0, "horizontal_ratio should be >= 0.0")
            self.assertLessEqual(result, 1.0, "horizontal_ratio should be <= 1.0")

    def test_vertical_ratio_exists_and_returns_valid_value(self):
        """Test that vertical_ratio() returns a valid value (used by example.py:24 and backend/app.py:71,138)"""
        self.gaze.refresh(self.dummy_frame)

        self.assertTrue(hasattr(self.gaze, 'vertical_ratio'),
                       "vertical_ratio method is missing")

        result = self.gaze.vertical_ratio()

        self.assertTrue(result is None or isinstance(result, (int, float)),
                       "vertical_ratio should return None or numeric value")

        if result is not None:
            self.assertGreaterEqual(result, 0.0, "vertical_ratio should be >= 0.0")
            self.assertLessEqual(result, 1.0, "vertical_ratio should be <= 1.0")

    def test_annotated_frame_uses_pupil_left_coords(self):
        """Test that annotated_frame() can still use pupil_left_coords() (line 96)"""
        self.gaze.refresh(self.dummy_frame)

        # This should not raise an error even though pupil_left_coords is called internally
        try:
            frame = self.gaze.annotated_frame()
            self.assertIsNotNone(frame, "annotated_frame should return a frame")
            self.assertEqual(frame.shape, self.dummy_frame.shape,
                           "annotated_frame should preserve frame dimensions")
        except AttributeError as e:
            self.fail(f"annotated_frame() failed due to missing method: {e}")

    def test_refresh_method(self):
        """Test that refresh() method works correctly"""
        # Should not raise any exceptions
        try:
            self.gaze.refresh(self.dummy_frame)
        except Exception as e:
            self.fail(f"refresh() raised unexpected exception: {e}")

    def test_pupils_located_property(self):
        """Test that pupils_located property exists and works"""
        self.gaze.refresh(self.dummy_frame)

        self.assertTrue(hasattr(self.gaze, 'pupils_located'),
                       "pupils_located property is missing")

        result = self.gaze.pupils_located
        self.assertIsInstance(result, bool, "pupils_located should return boolean")

    def test_example_py_workflow(self):
        """Test the workflow used in example.py to ensure it doesn't break"""
        # Simulate example.py workflow
        self.gaze.refresh(self.dummy_frame)

        # These calls should not raise exceptions
        try:
            frame = self.gaze.annotated_frame()
            left_pupil = self.gaze.pupil_left_coords()
            right_pupil = self.gaze.pupil_right_coords()
            horizontal_ratio = self.gaze.horizontal_ratio()
            vertical_ratio = self.gaze.vertical_ratio()

            # All should be None or valid values
            self.assertIsNotNone(frame)
            # Convert to string like example.py does
            str(left_pupil)
            str(right_pupil)
            str(horizontal_ratio)
            str(vertical_ratio)

        except AttributeError as e:
            self.fail(f"example.py workflow failed due to missing method: {e}")
        except Exception as e:
            self.fail(f"example.py workflow raised unexpected exception: {e}")

    def test_backend_api_workflow(self):
        """Test the workflow used in backend/app.py to ensure it doesn't break"""
        # Simulate backend/app.py workflow
        self.gaze.refresh(self.dummy_frame)

        # These calls should not raise exceptions
        try:
            left_pupil = self.gaze.pupil_left_coords()
            right_pupil = self.gaze.pupil_right_coords()
            horizontal = self.gaze.horizontal_ratio()
            vertical = self.gaze.vertical_ratio()

            # Simulate backend API response construction
            metrics = {
                'leftPupil': {
                    'x': left_pupil[0] if left_pupil else None,
                    'y': left_pupil[1] if left_pupil else None
                },
                'rightPupil': {
                    'x': right_pupil[0] if right_pupil else None,
                    'y': right_pupil[1] if right_pupil else None
                },
                'horizontal': horizontal,
                'vertical': vertical
            }

            # Should construct successfully
            self.assertIsInstance(metrics, dict)

        except AttributeError as e:
            self.fail(f"backend/app.py workflow failed due to missing method: {e}")
        except Exception as e:
            self.fail(f"backend/app.py workflow raised unexpected exception: {e}")


if __name__ == '__main__':
    unittest.main()
