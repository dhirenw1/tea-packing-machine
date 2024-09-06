#!/usr/bin/env python
import configparser
import yaml

CONFIG_FILE_PATH = '/home/tpm/tea-packing-machine/cfg/configuration.yaml'
class configuration:

    def __init__(self):
        # self.config = configparser.ConfigParser()
        # self.config.read(CONFIG_FILE_PATH)

        self._cfg = None

        with open(CONFIG_FILE_PATH) as f:
            self._cfg = yaml.load(f, Loader=yaml.FullLoader)
        
        print(self._cfg)
        
    def update(self, key, value):
        self._cfg[key] = value
        with open(CONFIG_FILE_PATH, 'w') as f:
            yaml.dump(self._cfg, stream=f, default_flow_style=False, sort_keys=False)