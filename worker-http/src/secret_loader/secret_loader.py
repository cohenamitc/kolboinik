import os
import logging

logger = logging.getLogger(__name__)

class SecretLoader():
    def __init__(self, secret_path: str, secret_name: str):
        self._secret_path = secret_path
        self._secret_name = secret_name
    
    def get_value(self) -> str:
        logger.info(f"Loading secret: {self._secret_path}{os.sep}{self._secret_name}")
        with open(f"{self._secret_path}{os.sep}{self._secret_name}", "r") as secret:
            return str(secret.read())