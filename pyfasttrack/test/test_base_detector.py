import pytest
import base_detector as detection
import cv2
import abc
import numpy as np
import scipy
import deepdiff


def instance():
    class DetectorInstance(detection.BaseDetector):
        def detect(self, image):
            return [(image, [666, 999])]

    return DetectorInstance()


def test_get_features():
    mask = cv2.imread("./test/data/rectangle_centered.png",
                      cv2.IMREAD_GRAYSCALE)
    detector = instance()
    test = detector.get_features(mask)
    assert pytest.approx(test["center"][0], 0.1) == 4166
    assert pytest.approx(test["center"][1], 0.1) == 4166
    mask = scipy.ndimage.shift(mask, (100, 0))
    test = detector.get_features(mask)
    assert pytest.approx(test["center"][0], 0.1) == 4166 + 100
    assert pytest.approx(test["center"][1], 0.1) == 4166


def test_get_orientation():
    mask = cv2.imread("./test/data/assymetric_left.png", cv2.IMREAD_GRAYSCALE)
    detector = instance()
    test = detector.get_features(mask)
    detector.get_direction(mask, test)
    assert pytest.approx(test["orientation"], 0.01) == pytest.approx(np.pi, 0.01)
    mask = scipy.ndimage.rotate(mask, 180)
    test = detector.get_features(mask)
    detector.get_direction(mask, test)
    assert pytest.approx(
        test["orientation"], .001) == pytest.approx(0, .001, abs=.1)
    mask = scipy.ndimage.rotate(mask, -90)
    test = detector.get_features(mask)
    detector.get_direction(mask, test)
    assert pytest.approx(test["orientation"],
                         0.01) == pytest.approx(3*np.pi*0.5, 0.01)


def test_process():
    mask = cv2.imread("./test/data/assymetric_left.png", cv2.IMREAD_GRAYSCALE)
    detector = instance()
    ref = detector.get_features(mask)
    ref["center"][0] += 666
    ref["center"][1] += 999
    detector.get_direction(mask, ref)
    test = detector.process(mask)
    assert not deepdiff.DeepDiff(
        ref, test[0]["2"], ignore_order=True, significant_digits=3)
