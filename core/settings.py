import logging


class Settings:
    PROJECT_NAME = "clickers"
    APP_NAME = "core"
    APP_INDEX = 0

    def __init__(self) -> None:
        # Настройки логгера
        self.LOG_FORMAT = "[%(asctime)s] - [%(levelname)s] - %(name)s -" \
                          " (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        self.LOG_FOLDER = "logs"
        self.CONSOLE_LOG_LEVEL = logging.DEBUG
        self.FILE_LOG_LEVEL = logging.DEBUG

        # Пути ресурсов
        self.RESOURCES_FOLDER = "resources"
        self.IMAGES_FOLDER = f"{self.RESOURCES_FOLDER}/images"

        # Шрифты
        self.FONTS = ["arial"]

    # noinspection PyPep8Naming
    @property
    def PRETTY_APP_NAME(self) -> str:
        # noinspection PyTypeChecker
        name = " ".join(map(str.capitalize, self.APP_NAME.split('_')))
        return f"{name} {self.APP_INDEX}"
