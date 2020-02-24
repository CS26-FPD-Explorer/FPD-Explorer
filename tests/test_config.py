import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from fpd_explorer import config_handler as config
import configparser


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
