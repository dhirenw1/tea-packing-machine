#!/usr/bin/env python
import configparser

CONFIG_FILE_PATH = '/home/tpm/tea-packing-machine/cfg/configuration.ini'
class configuration:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE_PATH)

    def update(self, section, key, value):
        self.config[section][key] = str(value)
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            self.config.write(configfile)