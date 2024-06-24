import json

from app.core.api.base_controller import logger
from app.core.common.log_models import SentryLog


class SentryQueuePublisher:

    @staticmethod
    def _get_sentry_queue_config(self):
        """
        Get the sentry queue configuration
        """
        pass

    def get_sentry_publisher(self):
        """
        Lazy-loads the sentry publisher
        """
        pass

    def set_sentry_publisher(self, publisher):
        """
        Setter method to the sentry publisher
        """
        pass


class SentryQueueService(SentryQueuePublisher):
    """
    A class that provides the sentry queue service
    """

    def _send_with_retries(self, message: str, retries: int = 5):
        """
        Send a log to the sentry service with retries
        """
        try:
            # Make sure the publisher is connected
            # self.get_sentry_publisher().send(message)
            pass
        except Exception as e:
            if retries > 0:
                # Reconnect the publisher before retrying
                # self.get_sentry_publisher().reconnect()
                self._send_with_retries(message, retries - 1)
            else:
                raise e

    def send_log(self, sentry_log: SentryLog):
        """
        Publish a log to the runningman service
        """
        json_string = json.dumps(sentry_log.model_dump(mode='json'))
        logger.info(f'process_name - {sentry_log.process_name}: Sending RunningMan Log: {json_string}')
        self._send_with_retries(json_string)
