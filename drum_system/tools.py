from typing import Tuple
import numpy as np
import math
import cv2 as cv


class Stick:
    """Class representing a drum stick with color detection and velocity calculation."""

    RED_HSV = np.array([[166, 84, 141], [186, 255, 255]])
    BLUE_HSV = np.array([[97, 100, 117], [117, 255, 255]])
    RED_RGB = (0, 0, 255)
    BLUE_RGB = (255, 0, 0)

    def __init__(self, color: str) -> None:
        """Initialize the Stick with a specific color."""
        self.color = color
        if color == "red":
            self.hsv = self.RED_HSV
            self.rgb = self.RED_RGB
        elif color == "blue":
            self.hsv = self.BLUE_HSV
            self.rgb = self.BLUE_RGB
        else:
            raise ValueError("Unsupported color")

        # To-do add enter time calculation
        # self.enter_time = 0
        self.velocity = 0
        self.last_5_centers = [(0, 0)] * 5
        self.tom2_hit = False
        self.tom1_hit = False
        self.hi_hat_hit = False
        self.snare_hit = False

    def calculate_velocity(self) -> None:
        """Calculate the velocity of the stick based on its last 5 positions."""
        x = (self.last_5_centers[4][0] - self.last_5_centers[2][0]) ** 2
        y = (
            self.last_5_centers[4][1] - self.last_5_centers[2][1]
        ) ** 2  # Fixed y component calculation
        self.velocity = round(math.sqrt(x + y))

    def update_centers(self, center: Tuple[int, int]) -> None:
        """Update the list of last 5 centers with a new center."""
        self.last_5_centers.pop(0)
        self.last_5_centers.append(center)

    def determine_volume(self) -> float:
        """Determine the volume based on the velocity."""
        volume = float(self.velocity / 50)
        return min(volume, 1.0)


class Drums:
    """Class representing the drum set with drawable areas."""

    def __init__(self) -> None:
        pass

    def draw_drum_areas(self, mat: np.ndarray) -> None:
        """Draw the drum areas on the given matrix."""
        cv.rectangle(mat, (50, 350), (200, 450), (88, 138, 122), 1)
        cv.rectangle(mat, (430, 350), (580, 450), (185, 122, 53), 1)
        cv.rectangle(mat, (80, 110), (230, 210), (160, 0, 160), 1)
        cv.rectangle(mat, (410, 110), (560, 210), (100, 120, 60), 1)
