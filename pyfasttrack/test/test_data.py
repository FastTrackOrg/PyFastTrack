import toml
import data
import deepdiff
import os
import shutil


def test_write_configuration():
    ref = toml.load("./test/data/cfg.toml")
    conf = data.Configuration()
    conf.read_toml("./test/data/cfg.toml")
    conf.write_toml("./test/data/_cfg.toml")
    test = toml.load("./test/data/_cfg.toml")
    os.remove("./test/data/_cfg.toml")
    assert ref == test


def test__get_key():
    ref = toml.load("./test/data/cfg.toml")["parameters"]
    conf = data.Configuration()
    conf.read_toml("./test/data/cfg.toml")
    assert ref["lightBack"] == conf.get_key("lightBack")
    assert [ref["lightBack"], ref["yTop"]
            ] == conf.get_keys(["lightBack", "yTop"])

def test_read_db():
    ref = toml.load("./test/data/cfg.toml")["parameters"]
    conf = data.Configuration()
    test = conf.read_db("./test/data/tracking.db")
    assert ref == test

def test_read_wrong():
    conf = data.Configuration()
    test = conf.read_db("./test/data/tracking_.db")
    assert test == None
    test = conf.read_toml("./test/data/cfg_.toml")
    assert test == None

def test_add_data_result():
    os.mkdir("./test/data/tmp/")
    result = data.Result("./test/data/tmp/")
    dat = dict()
    dat["head"] = {"center": (0, 0), "orientation": 0, "minor_axis": 1, "major_axis": 1}
    dat["body"] = {"center": (0, 0), "orientation": 0, "minor_axis": 1, "major_axis": 1}
    dat["tail"] = {"center": (0, 0), "orientation": 0, "minor_axis": 1, "major_axis": 1}
    dat["data"] = {"curv": 0, "area": 1, "perim": 1}
    dat["info"] = {"time": 1, "id": 1}
    test = result.add_data(dat)
    shutil.rmtree("./test/data/tmp/")
