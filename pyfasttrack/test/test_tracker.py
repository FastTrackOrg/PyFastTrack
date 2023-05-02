import pytest
from ..tracker import Tracker
import numpy as np


def test_max_dist():
    params = {"spot": "0", "normDist": 0, "normAngle": 0.5 *
              np.pi, "maxDist": 5, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (1, 1), "orientation": 45}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (3, 4), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (6, 6), "orientation": 180}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (2, 2), "orientation": 40}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (2, 3.5), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (7.5, 5), "orientation": 90}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == [0, 1, 2]


def test_max_dist_nq():
    params = {"spot": "0", "normDist": 0, "normAngle": 0.5 *
              np.pi, "maxDist": 1, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (1, 1), "orientation": 45}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (3, 4), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (6, 6), "orientation": 180}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (2, 2), "orientation": 40}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (2, 3.5), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (7.5, 5), "orientation": 90}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test != [0, 1, 2]


def test_empty_current():
    params = {"spot": "0", "normDist": 0, "normAngle": 0.5 *
              np.pi, "maxDist": 20, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (1, 1), "orientation": 45}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (3, 4), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (6, 6), "orientation": 180}, "3": {"area": 0, "perim": 0}}]
    current = []
    test = tracker.assign(past, current)
    assert test == [-1, -1, -1]


def test_new_object():
    params = {"spot": "0", "normDist": 0, "normAngle": 0.5 *
              np.pi, "maxDist": 0, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (1, 1), "orientation": 45}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (3, 4), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (6, 6), "orientation": 180}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (2, 2), "orientation": 40}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (2, 3.5), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (7.5, 5), "orientation": 90}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == [-1, -1, -1]


def test_one_object_lost():
    params = {"spot": "0", "normDist": 0, "normAngle": 0.5 *
              np.pi, "maxDist": 10, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (10, 10), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (30, 40), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (50, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (10, 15), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (35, 40), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (60, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == [0, 1, -1]


def test_all_lost():
    params = {"spot": "0", "normDist": 0, "normAngle": 0.5 *
              np.pi, "maxDist": 0, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (10, 10), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (30, 40), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (50, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (10, 15), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (35, 40), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (60, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == [-1, -1, -1]


def test_empty_prev():
    params = {"spot": "0", "normDist": 0, "normAngle": 0.5 *
              np.pi, "maxDist": 10, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = []
    current = [{"0": {"center": (10, 15), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (35, 40), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (60, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == []


def test_only_translation():
    params = {"spot": "0", "normDist": 1, "normAngle": 0,
              "maxDist": 20, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (10, 10), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (30, 40), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (50, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (50, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (10, 10), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (30, 40), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == [1, 2, 0]


def test_only_translation_nq():
    params = {"spot": "0", "normDist": 1, "normAngle": 0,
              "maxDist": 1, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (10, 10), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (30, 40), "orientation": 0}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (50, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (50, 50), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (10, 20), "orientation": 50}, "3": {
        "area": 0, "perim": 0}}, {"0": {"center": (50, 50), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test != [1, 2, 0]


def test_only_angle():
    params = {"spot": "0", "normDist": 10, "normAngle": 0.5 *
              np.pi, "maxDist": 20, "normArea": 0, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (10, 10), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (30, 40), "orientation": 3*0.5*np.pi},
                                                                                          "3": {"area": 0, "perim": 0}}, {"0": {"center": (50, 60), "orientation": 0.5*np.pi}, "3": {"area": 0, "perim": 0}}]
    current = [{"0": {"center": (60, 60), "orientation": 0}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (
        10, 0), "orientation": 0.5*np.pi}, "3": {"area": 0, "perim": 0}}, {"0": {"center": (30, 40), "orientation": 0}, "3": {"area": 0, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == [1, 2, 0]


def test_area():
    params = {"spot": "0", "normDist": 0, "normAngle": 0,
              "maxDist": 200, "normArea": 1, "normPerim": 0}
    tracker = Tracker(params)
    past = [{"0": {"center": (10, 10), "orientation": 10}, "3": {"area": 10, "perim": 0}}, {"0": {"center": (20, 20), "orientation": 20}, "3": {
        "area": 20, "perim": 0}}, {"0": {"center": (30, 30), "orientation": 30}, "3": {"area": 30, "perim": 0}}]
    current = [{"0": {"center": (20, 20), "orientation": 20}, "3": {"area": 20, "perim": 0}}, {"0": {"center": (30, 30), "orientation": 30}, "3": {
        "area": 30, "perim": 0}}, {"0": {"center": (10, 10), "orientation": 10}, "3": {"area": 10, "perim": 0}}]
    test = tracker.assign(past, current)
    assert test == [2, 0, 1]


def test_perim():
    params = {"spot": "0", "normDist": 0, "normAngle": 0,
              "maxDist": 200, "normArea": 0, "normPerim": 1}
    tracker = Tracker(params)
    past = [{"0": {"center": (10, 10), "orientation": 10}, "3": {"area": 0, "perim": 10}}, {"0": {"center": (20, 20), "orientation": 20}, "3": {
        "area": 0, "perim": 20}}, {"0": {"center": (30, 30), "orientation": 30}, "3": {"area": 0, "perim": 30}}]
    current = [{"0": {"center": (20, 20), "orientation": 20}, "3": {"area": 0, "perim": 20}}, {"0": {"center": (30, 30), "orientation": 30}, "3": {
        "area": 0, "perim": 30}}, {"0": {"center": (10, 10), "orientation": 10}, "3": {"area": 0, "perim": 10}}]
    test = tracker.assign(past, current)
    assert test == [2, 0, 1]


def test_reassign():
    tracker = Tracker()
    past = [0, 1, 2]
    current = [2, 1, 0]
    order = list(current)
    test = tracker.reassign(past, current, order)
    assert test == [0, 1, 2]
    past = [0, 1, 2]
    current = [3, 2, 1, 0]
    order = [3, 2, 1, -1]
    test = tracker.reassign(past, current, order)
    assert test == [0, 1, 2, 3]
    past = [1, 2, 3]
    current = []
    order = [-1, -1, -1]
    test = tracker.reassign(past, current, order)
    assert test == past
    past = [1, 2, 3]
    current = [3, 2]
    order = [-1, 1, 0]
    test = tracker.reassign(past, current, order)
    assert test == past
    past = [1, 2, 3]
    current = [3, 2, 4, 1]
    order = [3, 1, 0]
    test = tracker.reassign(past, current, order)
    assert test == [1, 2, 3, 4]
    past = [1, 2]
    current = [3, 2, 4, 1]
    order = [3, 1, -1, -1]
    test = tracker.reassign(past, current, order)
    assert test == [1, 2, 3, 4]


def test_find_lost():
    tracker = Tracker()
    prev = [1, 2, 3]
    current = [3, 2, 1]
    order = [2, 1, 0]
    assert tracker.reassign(prev, current, order) == prev
    assert tracker.find_lost(order) == []
    current = [3, 2]
    order = [-1, 1, 0]
    assert tracker.reassign(prev, current, order) == prev
    assert tracker.find_lost(order) == [0]
    current = [3]
    order = [-1, -1, 0]
    assert tracker.reassign(prev, current, order) == prev
    assert tracker.find_lost(order) == [0, 1]
    current = []
    order = [-1, -1, -1]
    assert tracker.reassign(prev, current, order) == prev
    assert tracker.find_lost(order) == [0, 1, 2]
    current = [3, 2, 4, 1]
    order = [3, 1, 0]
    assert tracker.reassign(prev, current, order) == [1, 2, 3, 4]
    assert tracker.find_lost(order) == []


def test_clean():
    tracker = Tracker()
    tracker.set_params({"maxTime": 0})
    current = [3, 2, 1]
    counter = [0, 0, 0]
    idty = [0, 1, 2]
    lost = []
    test_current, test_counter, test_idty = tracker.clean(
        current, counter, lost, idty)
    assert test_current == current
    assert test_counter == counter
    assert test_idty == idty
    tracker.set_params({"maxTime": 10})
    current = [3, 2, 1]
    counter = [0, 0, 0]
    idty = [0, 1, 2]
    lost = [1]
    test_current, test_counter, test_idty = tracker.clean(
        current, counter, lost, idty)
    assert test_current == current
    assert test_counter == [0, 1, 0]
    assert test_idty == idty
    tracker.set_params({"maxTime": 10})
    current = [3, 2, 1]
    counter = [1, 1, 0]
    idty = [0, 1, 2]
    lost = [0, 1]
    test_current, test_counter, test_idty = tracker.clean(
        current, counter, lost, idty)
    assert test_current == current
    assert test_counter == [2, 2, 0]
    assert test_idty == idty
    tracker.set_params({"maxTime": 10})
    current = [0, 1, 2]
    counter = [10, 0, 0]
    idty = [0, 1, 2]
    lost = [0]
    test_current, test_counter, test_idty = tracker.clean(
        current, counter, lost, idty)
    assert test_current == [1, 2]
    assert test_counter == [0, 0]
    assert test_idty == [1, 2]
    tracker.set_params({"maxTime": 10})
    current = [0, 1, 2]
    counter = [10, 10, 10]
    idty = [0, 1, 2]
    lost = [0, 1, 2]
    test_current, test_counter, test_idty = tracker.clean(
        current, counter, lost, idty)
    assert test_current == []
    assert test_counter == []
    assert test_idty == []
