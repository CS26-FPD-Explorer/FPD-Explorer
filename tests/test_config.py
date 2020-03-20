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
import configparser
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# First Party
from fpd_explorer import config_handler as config


test_file = "test.ini"


def test_if_default_exist():
    if os.path.isfile(config.DEFAULT_NAME):
        assert 1
    else:
        assert 0


def test_save_config():

    config.CONFIGFILE_NAME = test_file
    config._data_to_save.update({"Test": {"Bool": True}})
    config.save_config()

    config_parser = configparser.ConfigParser()
    config_parser.read(test_file)

    assert config_parser.getboolean("Test", "Bool")


def test_add_config():
    config.CONFIGFILE_NAME = test_file
    assert(config.add_config({"Test3": {"Bool": True}}))
    config.save_config()

    config_parser = configparser.ConfigParser()
    config_parser.read(test_file)

    assert config_parser.getboolean("Test3", "Bool")


def test_add_config_default():
    config.CONFIGFILE_NAME = test_file
    assert(config.add_config({"Bool": True}))
    config.save_config()

    config_parser = configparser.ConfigParser()
    config_parser.read(test_file)

    assert config_parser.getboolean("Default", "Bool")


def test_add_config_not_valid():
    config.CONFIGFILE_NAME = test_file
    assert not config.add_config("Wrong type")


def test_load_config():
    config.CONFIGFILE_NAME = test_file
    config_parser = configparser.ConfigParser()
    config_parser.add_section('Test2')
    config_parser.set('Test2', 'Bool2', "True")
    with open(test_file, 'w') as configfile:
        config_parser.write(configfile)
    config.load_config()
    assert config._data_to_save["Test2"]["bool2"]


def test_get_config():
    config._data_to_save.update({"Test3": {"bool3": True}})
    assert config.get_config("bool3")


def test_get_config_not_exit():
    assert not config.get_config("This does not exist")
