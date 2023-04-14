import toml
import data
import deepdiff
import os


def test_write_configuration():
    ref = toml.load("./test/data/cfg.toml")
    conf = data.Configuration()
    conf.read("./test/data/cfg.toml")
    conf.write("./test/data/_cfg.toml")
    test = toml.load("./test/data/_cfg.toml")
    os.remove("./test/data/_cfg.toml")
    assert ref == test


def test__get_key():
    ref = toml.load("./test/data/cfg.toml")["parameters"]
    conf = data.Configuration()
    conf.read("./test/data/cfg.toml")
    assert ref["lightBack"] == conf.get_key("lightBack")
    assert [ref["lightBack"], ref["yTop"]
            ] == conf.get_keys(["lightBack", "yTop"])
