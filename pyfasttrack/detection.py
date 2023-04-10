import abc
import numpy as np
import cv2
import scipy
import math


class Detector(metaclass=abc.ABCMeta):
    """Abstract class to implement an objects detector.

    """

    @abc.abstractmethod
    def detect(self, image):
        """Abstract method to be implemented.

        This method will take a full image with all the objects to detect and will return
        a list of tuples (mask, left_coordinate [x, y]) with one object by mask, the object represented by non-zero pixels
        and the background by zero pixels.


        Parameters
        ----------
        image : ndarray
            The full image.

        Returns
        -------
        dict
            Dictionnary containing the object features. Note that the direction is pi undertermined.

        """
        pass

    def process(self, image):
        """Process one image.

        Parameters
        ----------
        image : ndarray
            The full image.

        Returns
        -------
        lsit
            List of detected objects and their features.

        """
        detection = []
        for mask, coordinate in self.detect(image):
            features = self.get_features(mask)
            self.get_direction(mask, features)
            features["center"][0] += coordinate[0]
            features["center"][1] += coordinate[1]
            detection.append(features)
        return detection

    def get_features(self, mask):
        """Get the object features using equivalent ellipse.


        Parameters
        ----------
        mask : ndarray
            Mask of one object.

        """
        moments = cv2.moments(mask)

        x = moments["m10"] / moments["m00"]
        y = moments["m01"] / moments["m00"]

        i = moments["mu20"]
        j = moments["mu11"]
        k = moments["mu02"]

        if i + j - k != 0:
            orientation = (0.5 * np.arctan((2 * j) / (i - k)) +
                           (i < k) * (np.pi * 0.5))
            orientation += 2 * np.pi * (orientation < 0)
            orientation = (2 * np.pi - orientation)
        else:
            orientation = 0

        majAxis = 2 * \
            np.sqrt((((i + k) + np.sqrt((i - k) * (i - k) + 4 * j * j))
                    * 0.5) / moments["m00"])
        minAxis = 2 * \
            np.sqrt((((i + k) - np.sqrt((i - k) * (i - k) + 4 * j * j))
                    * 0.5) / moments["m00"])

        return {"center": [x, y], "orientation": orientation, "major_axis": majAxis, "minor_axis": minAxis}

    def modulo(self, angle):
        """Provide the mathematical 2pi modulo.


        Parameters
        ----------
        mask : float
            Angle in radian.

        Returns
        -------
        float
            Angle between 0->2pi

        """
        return angle - 2 * np.pi * math.floor(angle / (2 * np.pi))

    def get_direction(self, mask, features):
        """Get the object direction.

        The object orientation is updated with the correct direction.


        Parameters
        ----------
        mask : ndarray
            Mask of one object.
        features : dict
            Object features.

        """
        rotated_mask = scipy.ndimage.rotate(
            mask, (features["orientation"]*180)/np.pi)
        rotated_mask = np.sum(rotated_mask, axis=1, dtype=np.float64)
        rotated_mask /= np.sum(rotated_mask)
        indexes = np.arange(1, len(rotated_mask)+1, dtype=np.float64)
        mean = np.sum(indexes*rotated_mask)
        sd = np.sqrt(np.sum((indexes-mean)**2*rotated_mask))
        skew = (np.sum(indexes**3*rotated_mask) - 3 * mean * sd**2 - mean**3) / sd**3
        if skew > 0:
            features["orientation"] = self.modulo(
                features["orientation"] - np.pi)
