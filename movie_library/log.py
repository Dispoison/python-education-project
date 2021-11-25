"""Logging module"""

import logging
from os import path

from flask import Flask


class Log:
    """Logging class"""
    def __init__(self, app: Flask = None):
        """Constructor takes a string value of the application name"""
        self.file_path = path.dirname(__file__)
        self.log_path = None
        self.logger = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Configures the logger"""
        self.log_path = path.join(self.file_path, f'logs/{app.name}.log')
        self.logger = logging.getLogger(app.name)
        self.logger.handlers.clear()
        self.logger.setLevel(logging.INFO)
        f_handler = logging.FileHandler(self.log_path)
        f_handler.setLevel(logging.INFO)
        f_format = logging.Formatter('%(asctime)s - %(levelname)s - '
                                     '%(message)s', "%Y-%m-%d %H:%M:%S")
        f_handler.setFormatter(f_format)
        self.logger.addHandler(f_handler)

    def clear_log(self):
        """Clears log file"""
        with open(self.log_path, 'w', encoding='utf8'):
            pass
