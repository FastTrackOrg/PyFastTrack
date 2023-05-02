from pyfasttrack.yolo_detector import YoloDetector
from pyfasttrack.tracker import Tracker
from pyfasttrack.data import Result
import cv2
import os

example_folder_path = os.path.dirname(os.path.abspath(__file__))

# Data saver
saver = Result("{}/test/data/images/".format(example_folder_path))

# Set up detector
# See https://github.com/ultralytics/ultralytics/blob/44c7c3514d87a5e05cfb14dba5a3eeb6eb860e70/ultralytics/datasets/coco.yaml for equivalence between coco labels and indexes
yolo_params = {"model": "yolov8l-seg.pt", "classes": [2], "conf": 0.5}
detector = YoloDetector(yolo_params)

# Set up tracker
params = {"spot": 2, "normDist": 1, "normAngle": 2,
          "normArea": 1, "normPerim": 1, "maxDist": 500, "maxTime": 100}
tracker = Tracker()
tracker.set_params(params)
tracker.set_detector(detector)

camera = cv2.VideoCapture(
    "{}/test/data/images/Nascar.mp4".format(example_folder_path))
dat = tracker.initialize(camera.read()[1])
saver.add_data(dat)

ret = True
while (ret):
    ret, frame = camera.read()
    if ret:
        dat = tracker.process(frame)
        saver.add_data(dat)

camera.release()
