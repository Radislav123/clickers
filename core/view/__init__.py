import arcade

from core.settings import Settings
from logger import Logger


class View(arcade.View):
    settings = Settings()
    background_color = arcade.csscolor.DARK_SLATE_BLUE

    def __init__(self) -> None:
        self.logger = Logger(str(self.__class__))
        super().__init__()

    def on_show_view(self):
        self.window.background_color = self.background_color
        self.window.default_camera.use()
