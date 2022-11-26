import logging
import sys
import os

import requests

from config_loader import ConfigLoader
from secret_loader import SecretLoader
from service_bus import KolboinikServiceBus

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

service_config = ConfigLoader(os.environ.get("CONFIG_FILE", f"{os.sep}config{os.sep}config.json")).load_config()

class HttpWorker():
    def __init__(self):
        pass

    def get_message_from_queue(self):
        return KolboinikServiceBus(
            connection_string=SecretLoader(
                secret_path=service_config['secrets_path'],
                secret_name=service_config['service_bus']['connection_string']
            ).get_value(),
            queue_name=service_config['service_bus']['queue_name']
        ).receive_single_message()

    def make_request(self, method:str, url:str, headers:dict, data:str):
        logger.info(f"Sending HTTP {method} request to {url}")
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )
        if response.status_code < 400:
            logger.info(f"Received status code {response.status_code}")
        else:
            logger.warn(f"Received status code {response.status_code}")

    def run(self):
        logger.info("HTTP Worker initiated")
        try:
            task_config = self.get_message_from_queue()
        except IndexError as e:
            logger.warn("No messages found in queue, exiting")
            sys.exit(0)
        logger.info("Task config received from queue")
        inputs = dict(task_config['inputs'])

        # Support default values:
        inputs['method'] = inputs['method'] if 'method' in inputs.keys() else 'GET'
        inputs['body'] = inputs['body'] if 'body' in inputs.keys() else ''
        inputs['headers'] = inputs['headers'] if 'headers' in inputs.keys() else {}
        # End

        self.make_request(
            method=inputs['method'],
            url=inputs['targetUrl'],
            headers=inputs['headers'],
            data=inputs['body']
        )
