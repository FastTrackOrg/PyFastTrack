import toml
import data
import deepdiff
import os


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

