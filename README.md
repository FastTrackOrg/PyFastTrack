# PyFastTrack

[![Linux tests](https://github.com/FastTrackOrg/PyFastTrack/actions/workflows/linux_tests.yml/badge.svg)](https://github.com/FastTrackOrg/PyFastTrack/actions/workflows/linux_tests.yml) [![Windows tests](https://github.com/FastTrackOrg/PyFastTrack/actions/workflows/win_tests.yml/badge.svg)](https://github.com/FastTrackOrg/PyFastTrack/actions/workflows/win_tests.yml) [![Macos tests](https://github.com/FastTrackOrg/PyFastTrack/actions/workflows/macos_tests.yml/badge.svg)](https://github.com/FastTrackOrg/PyFastTrack/actions/workflows/macos_tests.yml) [![Documentation Status](https://readthedocs.org/projects/pyfasttrack/badge/?version=latest)](https://pyfasttrack.readthedocs.io/en/latest/?badge=latest)

## About

PyFastTrack is a Python library that provides an easy-to-use solution to integrate the FastTrack software tracking technology in Python projects. The tracking configuration and results will be entirely compatible with FastTrack.


## Roadmap

PyFastTrack is actively developed at a pace depending on the project [funding](https://ko-fi.com/bgallois). Follow [the FastTrack blog](https://www.fasttrack.sh/blog) for week-by-week updates. The development roadmap is as follows:
* ~~Abstract detection and tracking classes.~~
* ~~FastTrack detection and tracking classes one-to-one compatible with FastTrack.~~
* ~~Tracking data exportation base class compatible with FastTrack viewer.~~
* Optimization.
* First public release.
* YOLOv8 segmentation detector class.

## Usage

PyFastTrack can be integrated using the high-level API see [this example](https://github.com/FastTrackOrg/PyFastTrack/blob/master/pyfasttrack/example.py):

```python
import ft_detector as ft
import tracker as tr
import data as dat
import cv2

# Load configuration
config = dat.Configuration()
params = config.read_toml(
    "test/data/images/Groundtruth/Tracking_Result/cfg.toml")

# Set up saver
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
```

A low-level API is also available to subclass the Tracker class and reimplement the process method with a custom image analysis pipeline.
