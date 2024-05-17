import arcade
import arcade.gui

from core.settings import Settings


class Window(arcade.Window):
    settings = Settings()

    def __init__(self) -> None:
        super().__init__(
            self.settings.window.width,
            self.settings.window.height,
            self.settings.app_name,
            center_window = True
        )

        background_color = (255, 255, 255, 255)
        arcade.set_background_color(background_color)

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def on_draw(self) -> None:
        self.clear()

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        """Выводит в консоль положение курсора."""

        print(f"x: {x}, y: {y}")
