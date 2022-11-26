import logging

from azure.servicebus import ServiceBusClient, ServiceBusMessage

logger = logging.getLogger(__name__)

class KolboinikServiceBus():
    def __init__(self, connection_string, queue_name):
        self._client = ServiceBusClient.from_connection_string(conn_str=connection_string)
        self._sender = self._client.get_queue_sender(queue_name=queue_name)
        self._queue_name = queue_name

    def send_single_message(self, message):
        logger.info(f"Sending message to service bus {self._queue_name}: {message}")
        with self._sender:
            sb_message = ServiceBusMessage(message)
            self._sender.send_messages(sb_message)
        logger.info(f"Message sent")