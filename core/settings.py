import logging


class Settings:
    APP_NAME = "core"
    APP_INDEX = 0

    def __init__(self) -> None:
        # Настройки логгера
        self.LOG_FORMAT = "[%(asctime)s] - [%(levelname)s] - %(name)s -" \
                          " (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        self.LOG_FOLDER = "logs"
        self.CONSOLE_LOG_LEVEL = logging.DEBUG
        self.FILE_LOG_LEVEL = logging.DEBUG

        self.RESOURCES_FOLDER = "resources"
        self.IMAGES_FOLDER = f"{self.RESOURCES_FOLDER}/images"

    # noinspection PyPep8Naming
    @property
    def PRETTY_APP_NAME(self) -> str:
        return f"{self.APP_NAME.capitalize()} {self.APP_INDEX}"
