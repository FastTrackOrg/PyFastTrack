import ft_detector
import toml
import cv2
import pytest


def test_detect():
    params = toml.load("./test/data/cfg.toml")["parameters"]
    ft = ft_detector.FtDetector(params)
    background = cv2.imread("./test/data/background.pgm", cv2.IMREAD_GRAYSCALE)
    ft.set_background(background)
    image = cv2.imread("./test/data/frame.pgm", cv2.IMREAD_GRAYSCALE)
    test = ft.process(image)
    assert len(test) == 14
    assert pytest.approx(test[0]["2"]["center"][0],
                         0.0001) == pytest.approx(508.345, 0.0001)
    assert pytest.approx(test[0]["2"]["center"][1],
                         0.0001) == pytest.approx(330.876, 0.0001)
    assert pytest.approx(test[0]["2"]["orientation"],
                         0.00001) == pytest.approx(5.94395, 0.00001)
    # TODO: Precision not comparing with FastTrack C++
    assert pytest.approx(test[0]["0"]["center"][0],
                         0.001) == pytest.approx(514.327, 0.001)
    assert pytest.approx(test[0]["0"]["center"][1],
                         0.001) == pytest.approx(333.12, 0.001)
    assert pytest.approx(test[0]["0"]["orientation"],
                         0.001) == pytest.approx(5.81619, 0.001)
    assert pytest.approx(test[0]["1"]["center"][0],
                         0.001) == pytest.approx(499.96, 0.001)
    assert pytest.approx(test[0]["1"]["center"][1],
                         0.001) == pytest.approx(327.727, 0.001)
    assert pytest.approx(test[0]["1"]["orientation"],
                         0.01) == pytest.approx(6.10226, 0.01)
