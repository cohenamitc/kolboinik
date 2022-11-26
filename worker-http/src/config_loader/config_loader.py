import os
import json
import logging

logger = logging.getLogger(__name__)

class ConfigLoader():
    def __init__(self, config_path):
        self._config_path = config_path
    
    def load_config(self):
        logger.info(f'Loading service config from {self._config_path}')
        with open(self._config_path, 'r') as config_file:
            config_data = json.loads(config_file.read())
        return config_data