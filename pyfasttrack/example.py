from pyfasttrack.ft_detector import FtDetector
from pyfasttrack.tracker import Tracker
from pyfasttrack.data import Result
import data as dat
import cv2
import os

example_folder_path = os.path.dirname(os.path.abspath(__file__))

# Load configuration
config = dat.Configuration()
params = config.read_toml(
    "{}/test/data/images/Groundtruth/Tracking_Result/cfg.toml".format(example_folder_path))

# Data saver
saver = Result("{}/test/data/images/".format(example_folder_path))

# Set up detector
detector = FtDetector(params)
detector.set_background(cv2.imread(
    "{}/test/data/images/Groundtruth/Tracking_Result/background.pgm".format(example_folder_path), cv2.IMREAD_GRAYSCALE))

# Set up tracker
tracker = Tracker(params)
tracker.set_params(params)
tracker.set_detector(detector)

camera = cv2.VideoCapture(
    "{}/test/data/images/frame_%06d.pgm".format(example_folder_path))
dat = tracker.initialize(cv2.cvtColor(camera.read()[1], cv2.COLOR_BGR2GRAY))
saver.add_data(dat)

ret = True
while (ret):
    ret, frame = camera.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dat = tracker.process(frame)
        saver.add_data(dat)

camera.release()
