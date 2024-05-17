import arcade

from core.settings import Settings
from core.ui_manager import UIManager
from logger import Logger


class View(arcade.View):
    settings = Settings()
    background_color = (50, 50, 70, 255)

    def __init__(self) -> None:
        super().__init__()

        self.logger = Logger(str(self.__class__))
        self.ui_manager = UIManager()

    def on_show_view(self) -> None:
        self.window.background_color = self.background_color
        self.window.default_camera.use()
        self.ui_manager.enable()

    def on_hide_view(self) -> None:
        self.ui_manager.disable()

    def on_draw(self) -> None:
        self.clear()
        self.ui_manager.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        self.logger.debug(f"x: {x}, y: {y}")