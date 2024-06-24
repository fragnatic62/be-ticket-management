import json
from typing import TypeVar

from pydantic import BaseModel


IT = TypeVar('IT', bound=BaseModel)


class TMQueuePublisher:

    @staticmethod
    def _get_tm_queue_config(self):
        """
        Get the ticket management queue configuration
        """
        pass

    def get_tm_publisher(self):
        """
        Lazy-loads the ticket management publisher
        """
        pass

    def set_tm_publisher(self, publisher):
        """
        Setter method to the ticket management publisher
        """
        pass


class SentryQueueService(TMQueuePublisher):
    """
    A class that provides the sentry queue service
    """

    def _send_with_retries(self, message: str, retries: int = 5):
        """
        Send a log to the sentry service with retries
        """
        try:
            # Make sure the publisher is connected
            # self.get_tm_publisher().send(message)
            pass
        except Exception as e:
            if retries > 0:
                # Reconnect the publisher before retrying
                # self.get_tm_publisher().reconnect()
                self._send_with_retries(message, retries - 1)
            else:
                raise e

    def send_log(self, sentry_log: IT):
        """
        Publish a log to the tm queue service
        """
        json_string = json.dumps(sentry_log.model_dump(mode='json'))
        self._send_with_retries(json_string)
