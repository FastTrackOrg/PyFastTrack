import abc
import numpy as np
import cv2
import scipy
import math


class BaseDetector(metaclass=abc.ABCMeta):
    """Abstract class to implement an objects detector.

    """

    @abc.abstractmethod
    def detect(self, image):
        """Abstract method to be implemented.

        This method will take a full image with all the objects to detect and will return
        a list of tuples (mask, left_corner_coordinate [x, y]) with one object by mask, the object represented by non-zero pixels
        and the background by zero pixels.


        Parameters
        ----------
        image : ndarray
            The full image.

        Returns
        -------
        dict
            List of (mask, left_corner_coord).

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
        list
            List of detected objects and their features.

        """
        detections = []
        for mask, coordinate in self.detect(image):
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            data = {"area": cv2.contourArea(
                contours[0]), "perim": cv2.arcLength(contours[0], True)}

            body = self.get_features(mask)
            is_left, rotated_mask = self.get_direction(mask, body)
            body["center"][0] += coordinate[0]
            body["center"][1] += coordinate[1]

            mask_head = mask[:, 0:int(body["center"][0])]
            head = self.get_features(mask_head)
            """__, __ = self.get_direction(mask_head, head)
            head["center"][0] += coordinate[0]
            head["center"][1] += coordinate[1]"""
            # TODO with right coordinate

            mask_tail = mask[:, int(body["center"][0]):-1]
            tail = self.get_features(mask_tail)
            """__, __ = self.get_direction(mask_tail, tail)
            tail["center"][0] += coordinate[0] + body["center"][0]
            tail["center"][1] += coordinate[1]"""
            # TODO with right coordinate

            if is_left:
                detections.append({"3": data, "2": body, "1": tail, "0": head})
            else:
                detections.append({"3": data, "2": body, "2": tail, "1": head})
        return detections

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

    @staticmethod
    def modulo(angle):
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

        Returns
        -------
        bool
            Is object left oriented.
        ndarray
            Rotated mask.

        """
        rotated_mask = scipy.ndimage.rotate(
            mask, (features["orientation"]*180)/np.pi, reshape=False, order=0)
        rotated_mask = np.sum(rotated_mask, axis=1, dtype=np.float64)
        dist = rotated_mask / np.sum(rotated_mask)
        indexes = np.arange(1, len(dist)+1, dtype=np.float64)
        mean = np.sum(indexes*dist)
        sd = np.sqrt(np.sum((indexes-mean)**2*dist))
        skew = (np.sum(indexes**3*dist) -
                3 * mean * sd**2 - mean**3) / sd**3
        if skew > 0:
            features["orientation"] = self.modulo(
                features["orientation"] - np.pi)
            return True, rotated_mask
        else:
            return False, rotated_mask
