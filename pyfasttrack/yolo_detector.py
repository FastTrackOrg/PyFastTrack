from .base_detector import BaseDetector
import numpy as np
import cv2
from ultralytics import YOLO
import logging

logging.getLogger("ultralytics").setLevel(logging.WARNING)
logging.getLogger("tensorflow").setLevel(logging.WARNING)


class YoloDetector(BaseDetector):
    def __init__(self, params):
        """Initialize the detector.

        Parameters
        ----------
        params : dict
            Parameters.

        """
        self.params = params
        self.model = YOLO(self.params["model"])

    def detect(self, image):
        """Detect objects

        Parameters
        ----------
        image : ndarray
            Image as BGR.

        Returns
        -------
        list
            List of masks as [(mask, left_corner), ...].

        """
        results = self.model.predict(
            image, retina_masks=True, stream=True, **self.params)
        masks = [(np.moveaxis(np.uint8(i.masks.data.cpu().numpy()*255), 0, -1), (0, 0))
                 for i in next(results)]

        return masks
