import os
import logging
import traceback


class BaseCustomException(Exception):

    def __init__(self, message: str):
        self.message = f'[{self.__class__.__name__}: {message}]'

        # Get the filename where the exception was raised
        traceback_stack = traceback.extract_stack()
        filename = os.path.basename(traceback_stack[-2].filename)

        LOGGER = logging.getLogger(filename)
        LOGGER.debug(f'Exception encountered: {self.message}')

        super().__init__(self.message)
