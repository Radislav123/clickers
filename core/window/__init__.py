import arcade
import arcade.gui

from core.settings import Settings
from logger import Logger


class Window(arcade.Window):
    settings = Settings()
    width = 800
    height = 600
    background_color = (255, 255, 255, 255)

    def __init__(self) -> None:
        self.logger = Logger(str(self.__class__))
        super().__init__(
            self.width,
            self.height,
            self.settings.app_name,
            center_window = True
        )

        arcade.set_background_color(self.background_color)

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def on_draw(self) -> None:
        self.clear()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Выводит в консоль положение курсора."""

        print(f"x: {x}, y: {y}")
