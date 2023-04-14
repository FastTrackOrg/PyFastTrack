import toml


class Configuration():
    """Class to read and write configuration files compatible with FastTrack.

    """

    def read(self, path):
        """Read a configuration file.

        Parameters
        ----------
        path : str
            Path pointing to the toml file.

        """
        try:
            self.params = toml.load(path)
            return self.params
        except Exception as e:
            print(e)
            return None

    def write(self, path):
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
