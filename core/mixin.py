from arcade.gui import UIWidget

from core.settings import Settings
from core.service import Anchor


class MoveMixin(UIWidget):
    settings = Settings()

    def move_to(self, x: int, y: int, anchor_x: str, anchor_y: str) -> None:
        offset_x = x - self.x
        if anchor_x == Anchor.X.RIGHT:
            offset_x -= self.width

        offset_y = y - self.y
        if anchor_y == Anchor.Y.TOP:
            offset_y -= self.height

        self.move(offset_x, offset_y)
