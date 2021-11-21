"""Logging module"""

import logging
from os import path


class Log:
    """Logging class"""
    def __init__(self, app_name: str):
        """Constructor takes a string value of the application name"""
        self.file_path = path.dirname(__file__)
        self.file_name = path.join(self.file_path, f'{app_name}.log')
        self.logger = logging.getLogger(app_name)
        self.logger.handlers.clear()
        self._set_log()

    def _set_log(self):
        """Configures the logger"""
        self.logger.setLevel(logging.INFO)
        f_handler = logging.FileHandler(self.file_name)
        f_handler.setLevel(logging.INFO)
        f_format = logging.Formatter('%(asctime)s - %(levelname)s - '
                                     '%(message)s', "%Y-%m-%d %H:%M:%S")
        f_handler.setFormatter(f_format)
        self.logger.addHandler(f_handler)

    def clear_log(self):
        """Clears log file"""
        with open(self.file_name, 'w'):
            pass
