import toml
import sqlite3
import pathlib
import os
import numpy as np


class Configuration():
    """Class to read and write configuration files compatible with FastTrack.

    """

    def read_toml(self, path):
        """Read a configuration file from text file.

        Parameters
        ----------
        path : str
            Path pointing to the toml file.

        Returns
        -------
        Dict
            Parameters.

        """
        try:
            self.params = toml.load(path)
            return self.params
        except Exception as e:
            print(e)
            return None

    def read_db(self, path):
        """Read a configuration file from database.

        Parameters
        ----------
        path : str
            Path pointing to the sqlite database.

        Returns
        -------
        Dict
            Parameters.

        """
        try:
            cnx = sqlite3.connect(pathlib.Path(
                os.path.abspath(path)).as_uri() + "?mode=ro", uri=True)
            query = cnx.execute("SELECT parameter, value FROM parameter;")
            self.params = dict()
            for param, value in query:
                self.params[param] = value
            cnx.close()
            return self.params
        except Exception as e:
            print(e)
            return None

    def write_toml(self, path):
        """Write a configuration file.

        Parameters
        ----------
        path : str
            Path pointing to the toml file.

        """
        try:
            with open(path, 'w') as f:
                toml.dump(self.params, f)
        except Exception as e:
            print(e)

    def get_key(self, key):
        """Get a parameter from its key.

        Parameters
        ----------
        key : str
            Key.

        Returns
        -------
        Any
            Parameter.

        """
        return self.params["parameters"][key]

    def get_keys(self, keys):
        """Get parameters from their keys.

        Parameters
        ----------
        keys : list
            List of keys.

        Returns
        -------
        List
            Parameters.

        """
        return [self.params["parameters"][key] for key in keys]


class Result():
    """Class to write result files compatible with FastTrack.

    """

    def add_data(self, data):
        """Append data in the database.

            Parameters
            ----------
            data : dict
                Data.

        """
        query = self.cnx.execute("INSERT INTO tracking(xHead, yHead, tHead, xTail, yTail, tTail, xBody, yBody, tBody, curvature, areaBody,"
                                 "perimeterBody, headMajorAxisLength, headMinorAxisLength, headExcentricity, tailMajorAxisLength,"
                                 "tailMinorAxisLength, tailExcentricity, bodyMajorAxisLength, bodyMinorAxisLength, bodyExcentricity,"
                                 "imageNumber, id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                                 (data["head"]["center"][0], data["head"]["center"][1], data["head"]["orientation"],
                                  data["tail"]["center"][0], data["tail"]["center"][1], data["tail"]["orientation"],
                                  data["body"]["center"][0], data["body"]["center"][1], data["body"]["orientation"],
                                  data["data"]["curv"], data["data"]["area"], data["data"]["perim"],
                                  data["head"]["major_axis"], data["head"]["minor_axis"], np.sqrt(
                                     1-(data["head"]["minor_axis"]/data["head"]["major_axis"])**2),
                                  data["tail"]["major_axis"], data["tail"]["minor_axis"], np.sqrt(
                                     1-(data["tail"]["minor_axis"]/data["tail"]["major_axis"])**2),
                                  data["body"]["major_axis"], data["body"]["minor_axis"], np.sqrt(
                                     1-(data["body"]["minor_axis"]/data["body"]["major_axis"])**2),
                                  data["info"]["time"], data["info"]["id"]))

    def __init__(self, path):
        self.cnx = sqlite3.connect(os.path.abspath(path) + "/tracking.db")
        query = self.cnx.execute("CREATE TABLE tracking ( xHead REAL, yHead REAL, tHead REAL, xTail REAL,"
                                 "yTail REAL, tTail REAL, xBody REAL, yBody REAL, tBody REAL,"
                                 "curvature REAL, areaBody REAL, perimeterBody REAL,"
                                 "headMajorAxisLength REAL, headMinorAxisLength REAL,"
                                 "headExcentricity REAL, tailMajorAxisLength REAL, tailMinorAxisLength REAL,"
                                 "tailExcentricity REAL, bodyMajorAxisLength REAL, bodyMinorAxisLength REAL,"
                                 "bodyExcentricity REAL, imageNumber INTEGER, id INTEGER)")

    def __del__(self):
        self.cnx.close()
