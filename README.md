# PyFastTrack

## About

PyFastTrack is a Python library that provides an easy-to-use solution to integrate the FastTrack software tracking technology in Python projects. The tracking parameters configuration and the tracking results will be entirely compatible with FastTrack.

## Usage

PyFastTrack can be integrated using the high-level API:

```python
import cv2
import numpy as np
import pyfasttrack as ft

tracker = ft.Tracker()
tracker.load_parameters("params.toml")
tracker.load_background("background.pgm")
tracker.set_saving("data.db", with_image=True)

camera = cv2.VideoCapture(0)
tracker.initialize(camera.read()[1])

while(True):
	ret, frame = camera.read()
	if not ret:
		return
	data = tracker.process(frame)
	# Data can be consumed here
```

A low-level API is also available to subclass the Tracker class and reimplement the process method with a custom image analysis pipeline.

![alt text](./docs/imgs/pyfasttrack_api.png)
