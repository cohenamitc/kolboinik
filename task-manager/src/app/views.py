import os 
import sys
import logging
import json
import pathlib
from datetime import datetime
from uuid import uuid4

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

def error_reply(message:str, request_id:str, http_status_code:int=400) -> jsonify:
    return jsonify(
        status="error",
        timestamp=str(datetime.now()),
        request_id=request_id,
        message=message
    ), http_status_code
    

@app.route('/job_config', methods=['GET', 'POST'])
def job_config():
    request_id = str(uuid4())
    if request.method == 'POST':
        data = None
        # Get JSON config
        if request.is_json:
            data = request.get_json(silent=True)
            if not data:
                return error_reply(
                    message="Couldn't parse JSON input", 
                    request_id=request_id
                    )
        # Get YAML config
        if request.headers.get('Content-Type', '') == 'application/yaml':
            data = yaml.safe_load(request.get_data(as_text=True))
        if not data:
            return error_reply(
                message="Something went wrong",
                request_id=request_id
                )
        
        KolboinikServiceBus(
            connection_string=SecretLoader(secret_path=service_config['secrets_path'], secret_name=service_config['service_bus']['connection_string']).get_value(),
            queue_name=data['kind']
            ).send_single_message(message=json.dumps(data))

        return jsonify(
            status='ok',
            timestamp=str(datetime.now()),
            request_id=request_id,
            message=data
        )
    return error_reply(message="No change made, this endpoint accepts POST messages only")
