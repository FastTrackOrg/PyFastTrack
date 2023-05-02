from .base_detector import BaseDetector
import numpy as np
import cv2


class FtDetector(BaseDetector):
    def __init__(self, params):
        self.params = params

    def detect(self, image):
        if int(self.params["lightBack"]) == 0:
            image = cv2.subtract(self.background, image)
        else:
            image = cv2.subtract(image, self.background)

        __, image = cv2.threshold(image, int(
            self.params["thresh"]), 255, cv2.THRESH_BINARY)

        if int(self.params["morphSize"]) != 0 and int(self.params["morph"]) != 8:
            element = cv2.getStructuringElement(int(self.params["morphType"]), (2 * int(self.params["morphSize"]) + 1, 2 * int(
                self.params["morphSize"]) + 1), (int(self.params["morphSize"]), int(self.params["morphSize"])))
            image = cv2.morphologyEx(image, int(self.params["morph"]), element)

        if int(self.params["xBottom"]) != 0 and int(self.params["yBottom"]) != 0:
            image = image[int(self.params["yTop"]):int(self.params["yBottom"]), int(
                self.params["xTop"]):int(self.params["xBottom"])]

        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        masks = []
        for i in contours:
            area = cv2.contourArea(i)
            if area < int(self.params["maxArea"]) and area > int(self.params["minArea"]):
                rect = cv2.boundingRect(i)
                mask = np.zeros_like(image)
                cv2.drawContours(mask, [i], 0, 255, -1, 8)
                masks.append(
                    (np.copy(mask[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]), rect[0:2]))

        return masks

    def set_background(self, image):
        self.background = np.copy(image)
