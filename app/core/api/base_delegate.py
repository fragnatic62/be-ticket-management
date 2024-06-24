import os
from abc import ABC, abstractmethod
from typing import Optional, Mapping, Any
from uuid import uuid4

from app.core.common.base_schema import APIProcessReport
from app.core.common.log_models import SentryLog, LogTypeOptions


class BaseAPIControllerDelegate(ABC):
    """
    Delegate interface for API controller events.

    Attributes:
        _full_dir (str): The full path of the delegate class file.
        _sentry_enabled (bool): Whether sending logs to runningman is enabled.
        _process_name_prefix (str): The prefix for the process

    Methods:
        on_process_failure(self, report: APIProcessReport) -> None:
            Called when an API process encounters an error.

        on_process_finished(self, report: APIProcessReport) -> None:
            Called when an API process is finished.

    Note:
        - This class is an interface defining the methods that should
          be implemented by delegate classes.
        - Implementing subclasses should override the `on_process_finished`
          method to handle the event
          when an API process is finished.

    """
    _full_dir: str = __file__
    _sentry_enabled: bool = False
    _process_name_prefix: str = 'mvs_api'
    _data_id_prefix: str = 'mvs'
    _company_default: str = 'mvs_api'
    _retailer_default: str = 'mvs_api'

    @abstractmethod
    def on_process_failure(self, report: APIProcessReport) -> None:
        """
        Called when an API process is finished.

        Args:
            report (APIProcessReport): The APIProcessReport containing the
            result of the finished process.

        """
        raise NotImplementedError

    @abstractmethod
    def on_process_finished(self, report: APIProcessReport) -> None:
        """
        Called when an API process is finished.

        Args:
            report (APIProcessReport): The APIProcessReport containing the
            result of the finished process.

        """
        raise NotImplementedError

    def _create_sentry_log(self, report: APIProcessReport, log_type: LogTypeOptions) -> SentryLog:
        return SentryLog(
            data_id=f'{self._data_id_prefix}_{str(uuid4())}',
            company=self._company_default,
            retailer=self._retailer_default,
            process_name=f'{self._process_name_prefix.lower()}_{self.get_controller_name()}',
            log_type=log_type,
            payload=self._serialize_to_log_payload(report),
            error=report.message
        )

    @staticmethod
    def _serialize_to_log_payload(report: Optional[APIProcessReport]) -> Mapping[str, Any]:
        """
        Serialize API response payload for logging purposes.

        This method converts the API response payload into a format suitable for
        inclusion in Running Man logs. If the payload is a list, each element is
        serialized using the `model_dump` method.

        Parameters:
            report (Optional[APIProcessReport]): The APIProcessReport containing

        Returns:
            Mapping[str, Any]: The serialized payload.
        """
        if report.status_code in [200, 201] and report.response:
            return report.response.model_dump()
        return report.model_dump()

    def get_controller_name(self) -> str:
        """
        Get the name of the controller from the full path of the delegate class file.

        This method extracts the name of the controller from the full path of
        the delegate class file. It is used to create the process name for
        Running Man logs.

        Returns:
            str: The name of the controller.
        """
        full_path: str = os.path.realpath(self._full_dir)
        path: str = os.path.split(full_path)[0]
        return path.split(os.sep)[-1:][0]
