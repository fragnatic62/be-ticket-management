from app.services.sentry.service import SentryQueueService


class SentryQueuePublisher:
    """
    A class that provides the RMQ publisher
    """
    _sentry_publisher: SentryQueueService = None

    def get_sentry_publisher(self):
        """
        Lazy-loads the RMQ publisher.
        """
        if not self._sentry_publisher:
            self._sentry_publisher = SentryQueueService()
        return self._sentry_publisher

    def set_sentry_publisher(self, publisher: SentryQueueService):
        """
        Setter method to the RMQ publisher.
        """
        self._sentry_publisher = publisher
