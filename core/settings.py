import dataclasses
import json


@dataclasses.dataclass
class Window:
    width: int
    height: int


class Settings:
    APP_NAME = "core"
    window_class = Window
    window: window_class

    def __init__(self) -> None:
        self.update_settings()

    # noinspection PyPep8Naming
    @property
    def SETTINGS_PATH(self) -> str:
        return f"{self.APP_NAME}/settings.json"

    def update_settings(self) -> None:
        with open(self.SETTINGS_PATH, 'r') as file:
            settings_json = json.load(file)
            self.window = self.window_class(**settings_json["window"])
