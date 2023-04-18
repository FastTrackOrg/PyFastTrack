import toml
import sqlite3
import pathlib
import os


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
            cnx = sqlite3.connect(pathlib.Path(os.path.abspath(path)).as_uri() + "?mode=ro", uri = True)
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
