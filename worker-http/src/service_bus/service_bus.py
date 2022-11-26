import logging
import json

from azure.servicebus import ServiceBusClient

logger = logging.getLogger(__name__)

class KolboinikServiceBus():
    def __init__(self, connection_string, queue_name, max_wait_time=5):
        self._client = ServiceBusClient.from_connection_string(conn_str=connection_string)
        self._receiver = self._client.get_queue_receiver(queue_name=queue_name, max_wait_time=max_wait_time)
        self._queue_name = queue_name
    
    def receive_single_message(self):
        logger.info(f"Receiving 1 message from {self._queue_name}")
        with self._receiver:
            message = self._receiver.receive_messages(max_message_count=1)[0]
            self._receiver.complete_message(message=message)
            return json.loads(str(message))
