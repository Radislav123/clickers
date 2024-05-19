from arcade.gui import UIFlatButton

from core.mixin import MovableWidgetMixin
from core.service import Color
from core.settings import Settings


class FlatButton(UIFlatButton, MovableWidgetMixin):
    settings = Settings()

    # todo: обновить, опираясь на TextureButton.DEFAULT_STYLE
    NORMAL_STYLE = UIFlatButton.UIStyle(font_size = 12, bg = Color.NORMAL)
    HOVERED_STYLE = UIFlatButton.UIStyle(font_size = 14, bg = Color.HOVERED)
    PRESSED_STYLE = UIFlatButton.UIStyle(font_size = 12, bg = Color.PRESSED)
    DISABLED_STYLE = UIFlatButton.UIStyle(font_size = 12, bg = Color.DISABLED)
    DEFAULT_STYLE = {
        "normal": NORMAL_STYLE,
        "hover": HOVERED_STYLE,
        "press": PRESSED_STYLE,
        "disabled": DISABLED_STYLE
    }
