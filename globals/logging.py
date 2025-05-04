from .globals import LOG_PATH
from datetime import datetime


class LoggingMixin:
    def info(self, message: str):
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"{datetime.now()} [INFO] {message}")

    def error(self, message: str):
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"{datetime.now()} [ERROR] {message}")
