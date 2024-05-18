import arcade
from arcade.gui import UIWidget

from core.service import Anchor
from core.settings import Settings


class MovableWidgetMixin(UIWidget):
    settings = Settings()

    def move_to(self, x: int, y: int, anchor_x: str, anchor_y: str) -> None:
        offset_x = x - self.x
        if anchor_x == Anchor.X.RIGHT:
            offset_x -= self.width
        elif anchor_x == Anchor.X.CENTER:
            offset_x -= self.width / 2

        offset_y = y - self.y
        if anchor_y == Anchor.Y.TOP:
            offset_y -= self.height
        elif anchor_y == Anchor.Y.CENTER:
            offset_y -= self.height / 2

        self.move(offset_x, offset_y)

    def center_on_screen(self) -> None:
        center_x = arcade.get_window().width // 2
        center_y = arcade.get_window().height // 2

        self.move_to(center_x, center_y, Anchor.X.CENTER, Anchor.Y.CENTER)
