import ft_detector as ft
import tracker as tr
import data as dat
import cv2

# Load configuration
config = dat.Configuration()
params = config.read_toml(
    "test/data/images/Groundtruth/Tracking_Result/cfg.toml")

saver = dat.Result("test/data/images/")

# Set up detector
detector = ft.FtDetector(params)
detector.set_background(cv2.imread(
    "test/data/images/Groundtruth/Tracking_Result/background.pgm", cv2.IMREAD_GRAYSCALE))

# Set up tracker
tracker = tr.Tracker(params)
tracker.set_params(params)
tracker.set_detector(detector)

camera = cv2.VideoCapture("test/data/images/frame_%06d.pgm")
tracker.initialize(cv2.cvtColor(camera.read()[1], cv2.COLOR_BGR2GRAY))

ret = True
while (ret):
    ret, frame = camera.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dat = tracker.process(frame)
        saver.add_data(dat)

camera.release()
