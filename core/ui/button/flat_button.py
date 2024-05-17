from arcade.gui import UIFlatButton
from core.mixin import MoveMixin

from core.settings import Settings


class FlatButton(UIFlatButton, MoveMixin):
    settings = Settings()

    normal_style = UIFlatButton.UIStyle(bg = (58, 58, 78, 255))
    hovered_style = UIFlatButton.UIStyle(bg = (64, 64, 86, 255))
    pressed_style = UIFlatButton.UIStyle(bg = (40, 40, 60, 255))
    disabled_style = UIFlatButton.UIStyle(bg = (72, 72, 84, 255))
    default_style = {
        "normal": normal_style,
        "hover": hovered_style,
        "press": pressed_style,
        "disabled": disabled_style
    }

    def __init__(self, **kwargs) -> None:
        if "style" not in kwargs:
            kwargs["style"] = self.default_style
        super().__init__(**kwargs)
