import os 
import sys
import logging
import json
import pathlib

from flask import jsonify, request
import yaml

from . import app

from secret_loader import SecretLoader
from service_bus import KolboinikServiceBus
from config_loader import ConfigLoader

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.config["DEBUG"] = os.environ.get("ENV", "").lower() == "dev"

service_config = ConfigLoader(os.environ.get('CONFIG_FILE', f'{pathlib.Path(__file__).parent.resolve()}{os.sep}..{os.sep}config.json')).load_config()

def error_reply(message:str, http_status_code=400) -> jsonify:
    return jsonify(
        status="error",
        message=message
    ), http_status_code

def load_config():
    global service_config
    

@app.route('/job_config', methods=['GET', 'POST'])
def job_config():
    if request.method == 'POST':
        data = None
        # Get JSON config
        if request.is_json:
            data = request.get_json(silent=True)
            if not data:
                return error_reply("Couldn't parse JSON input")
        # Get YAML config
        if request.headers.get('Content-Type', '') == 'application/yaml':
            data = yaml.safe_load(request.get_data(as_text=True))
        if not data:
            return error_reply("Something went wrong")
        
        KolboinikServiceBus(
            connection_string=SecretLoader(secret_path=service_config['secrets_path'], secret_name=service_config['service_bus']['connection_string']).get_value(),
            queue_name=data['kind']
            ).send_single_message(message=json.dumps(data))

        return jsonify(dict(data))
    return jsonify(
        status="Bad request",
        message="No change made, this endpoint accepts POST messages only"
        ), 400

if __name__ == "__main__":
    logger.info('Starting app')
    load_config()
    app.run()
