
from app.core.api.base_delegate import BaseAPIControllerDelegate
from app.core.common.base_schema import APIProcessReport
from app.core.common.log_models import LogTypeOptions


class APIControllerDelegate(BaseAPIControllerDelegate):
    """
    Delegate class for handling when an API invocation to get the list of tasks
    either succeed or fail.
    """
    _full_dir: str = __file__

    def on_process_failure(self, report: APIProcessReport) -> None:
        """
        Handle the event when an error occurs during data processing.
        """
        _rm_log = self._create_sentry_log(report, LogTypeOptions.ERROR)
        if self._sentry_enabled:
            pass
            # self.get_sentry_service().send_log(_rm_log)

    def on_process_finished(self, report: APIProcessReport) -> None:
        """
        Handle the event when a data processing operation is successfully finished.
        """
        _rm_log = self._create_sentry_log(report, LogTypeOptions.SUCCESS)
        if self._sentry_enabled:
            pass
            # self.get_sentry_service().send_log(_rm_log)
