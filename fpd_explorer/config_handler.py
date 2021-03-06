# Copyright 2019-2020 Florent AUDONNET, Michal BROOS, Bruce KERR, Ewan PANDELUS, Ruize SHEN

# This file is part of FPD-Explorer.

# FPD-Explorer is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# FPD-Explorer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with FPD-Explorer.  If not, see < https: // www.gnu.org / licenses / >.

# Standard Library
import os
import configparser

CONFIGFILE_NAME = "config.ini"

_data_to_save = {'Default': {}}


def get_config(key_to_get: str):
    """
    Get a config setting with the given key.

    Parameters
    ----------
    key_to_get : str
        Key of the value as given in the add config
    """
    def _finditem(key, obj=_data_to_save):
        """
        Return the item for a given key, else None.
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
    Return either the dict for the given key or an empty dict.
    """
    return _data_to_save.get(key_to_get, {})


def add_config(config: dict):
    """
    Add the config dict to the save file.

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
    Load the configuration file.
    """
    global _data_to_save

    def as_dict(config):
        """
        Convert a ConfigParser object into a dictionary.

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
                if isinstance(val, str) and val.isdigit():
                    val = float(val)
                the_dict[section][key] = val
        return the_dict

    if os.path.isfile(CONFIGFILE_NAME):
        config = configparser.ConfigParser()
        config.read(CONFIGFILE_NAME)
        _data_to_save.update(as_dict(config))
    else:
        _data_to_save.update({"Appearence": {"dark_mode":  False}})



def save_config():
    """
    Save the full config to a file.
    """
    prev_config = None
    if os.path.isfile(CONFIGFILE_NAME):
        with open(CONFIGFILE_NAME, "r") as f:
            prev_config = f.read()
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
