# Standard Library
import os
import sys
import configparser

CONFIGFILE_NAME = "config.ini"
DEFAULT_NAME = "default.ini"

_data_to_save = {}


def get_config(key_to_get: str):
    """
    Get a config setting with the given key

    Parameters
    ----------
    key_to_get : str
        Key of the value as given in the add config
    """
    def _finditem(key, obj=_data_to_save):
        """
        Return the item for a given key
        else none
        """
        if key in obj:
            return obj[key]
        for k, v in obj.items():
            if isinstance(v, dict):
                item = _finditem(key, v)
                if item is not None:
                    return item
    return _finditem(key_to_get)


def get_dict(key_to_get: str) -> dict:
    """
    Return either the dict for the given key or an empty dict
    """
    return _data_to_save.get(key_to_get, {})


def add_config(config: dict):
    """
    Add some config to the save file

    Parameters
    ----------
    config : dict
        dict must be configure as:
            key = parameter
            value = value
        key can also be a section in which case value must be another dict respecting the upward configuration
        Example :
        {
            Appearence:
            {
                dark_mode:True
            }
        }
    """
    print("Saving new value")
    if isinstance(config, dict):
        if isinstance(list(config.values())[0], dict):
            # already have a section so we can just update
            _data_to_save.update(config)
            return True
        else:
            _data_to_save["Default"].update(config)
            return True
    return False


def load_config():
    """
    Load the configuration file
    """
    global _data_to_save

    def as_dict(config):
        """
        Converts a ConfigParser object into a dictionary.

        The resulting dictionary has sections as keys which point to a dict of the
        sections options as key => value pairs.
        """
        the_dict = {}
        for section in config.sections():
            the_dict[section] = {}
            for key, val in config.items(section):
                if val.lower() in ["true", "yes"]:
                    val = True
                elif val.lower() in ["false", "no"]:
                    val = False
                the_dict[section][key] = val
        return the_dict

    path_to_read = ""
    if os.path.isfile(CONFIGFILE_NAME):
        path_to_read = CONFIGFILE_NAME
    else:
        path_to_read = DEFAULT_NAME

    config = configparser.ConfigParser()
    config.read(path_to_read)
    print("Loading configs")
    _data_to_save.update(as_dict(config))


def save_config():
    """
    Save all the config to file
    """
    prev_config = None
    if os.path.isfile(CONFIGFILE_NAME):
        with open(CONFIGFILE_NAME, "r") as f:
            prev_config = f.read()
    print("Saving....")
    # Create the configuration file as it doesn't exist yet
    with open(CONFIGFILE_NAME, "w") as f:
        try:
            # Add content to the file
            if not isinstance(list(_data_to_save.values())[0], dict):
                # there is no sections
                tmp_dict = {
                    "Default": _data_to_save
                }
            else:
                tmp_dict = _data_to_save

            config = configparser.ConfigParser()
            config.read_dict(tmp_dict)
            config.write(f)
        except BaseException:
            if prev_config:
                f.write(prev_config)
                print("Unexpected error:", sys.exc_info())
