import abc
import numpy as np
import cv2


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
            is_left, rotated_mask, rot = self.get_direction(mask, body)

            body_center = np.intp(
                rot @ np.asarray([body["center"][0], body["center"][1], 1]))
            rot = cv2.invertAffineTransform(rot)

            mask_tail = rotated_mask[:, body_center[0]::]
            tail = self.get_features(mask_tail)
            a = rot @ np.asarray(
                [tail["center"][0] + body_center[0], tail["center"][1], 1])
            tail["center"][0] = a[0] + coordinate[0]
            tail["center"][1] = a[1] + coordinate[1]
            tail["orientation"] = tail["orientation"] - \
                np.pi * (tail["orientation"] > np.pi)
            tail["orientation"] = self.modulo(
                tail["orientation"] + body["orientation"] + np.pi * (np.abs(tail["orientation"]) > 0.5 * np.pi))

            mask_head = rotated_mask[:, 0:body_center[0]]
            head = self.get_features(mask_head)
            a = rot @ np.asarray([head["center"][0], head["center"][1], 1])
            head["center"][0] = a[0] + coordinate[0]
            head["center"][1] = a[1] + coordinate[1]
            head["orientation"] = head["orientation"] - \
                np.pi * (head["orientation"] > np.pi)
            head["orientation"] = self.modulo(
                head["orientation"] + body["orientation"] + np.pi * (np.abs(head["orientation"]) > 0.5 * np.pi))

            body["center"][0] += coordinate[0]
            body["center"][1] += coordinate[1]

            if is_left:
                detections.append({"3": data, "2": body, "1": tail, "0": head})
            else:
                detections.append({"3": data, "2": body, "0": tail, "1": head})
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

        maj_axis = 2 * \
            np.sqrt((((i + k) + np.sqrt((i - k) * (i - k) + 4 * j * j))
                    * 0.5) / moments["m00"])
        min_axis = 2 * \
            np.sqrt((((i + k) - np.sqrt((i - k) * (i - k) + 4 * j * j))
                    * 0.5) / moments["m00"])

        return {"center": [x, y], "orientation": orientation, "major_axis": maj_axis, "minor_axis": min_axis}

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
        return angle - 2 * np.pi * np.floor(angle / (2 * np.pi))

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
        ndarray
            Rotation matrix.

        """
        rot = cv2.getRotationMatrix2D(center=(
            mask.shape[1]/2, mask.shape[0]/2), angle=-(features["orientation"]*180)/np.pi, scale=1)
        new_size = [mask.shape[0]*np.abs(rot[0, 1]) + mask.shape[1]*np.abs(rot[0, 0]),
                    mask.shape[0]*np.abs(rot[0, 0]) + mask.shape[1]*np.abs(rot[0, 1])]
        rot[0, 2] += new_size[0]/2 - mask.shape[1]/2
        rot[1, 2] += new_size[1]/2 - mask.shape[0]/2
        rotated_mask = cv2.warpAffine(mask, rot, np.intp(new_size))
        dist = np.sum(rotated_mask, axis=0, dtype=np.float64)
        dist /= np.sum(dist)
        indexes = np.arange(1, len(dist)+1, dtype=np.float64)
        mean = np.sum(indexes*dist)
        sd = np.sqrt(np.sum((indexes-mean)**2*dist))
        skew = (np.sum(indexes**3*dist) -
                3 * mean * sd**2 - mean**3) / sd**3
        if skew > 0:
            features["orientation"] = self.modulo(
                features["orientation"] - np.pi)
            return True, rotated_mask, rot
        else:
            return False, rotated_mask, rot
