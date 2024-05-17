import logging


class Settings:
    app_name = "core"

    def __init__(self) -> None:
        # Настройки логгера
        self.LOG_FORMAT = "[%(asctime)s] - [%(levelname)s] - %(name)s -" \
                          " (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        self.LOG_FOLDER = "logs"
        self.CONSOLE_LOG_LEVEL = logging.DEBUG
        self.FILE_LOG_LEVEL = logging.DEBUG
