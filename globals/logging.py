from .globals import LOG_PATH
from django.utils import timezone


class LoggingMixin:
    def info(self, message: str):
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"{timezone.now()} [INFO] {message}")

    def error(self, message: str):
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"{timezone.now()} [ERROR] {message}")
