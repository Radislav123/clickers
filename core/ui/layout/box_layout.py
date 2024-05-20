from arcade.gui import UIBoxLayout

from core.mixin import MovableWidgetMixin
from core.settings import Settings


class BoxLayout(UIBoxLayout, MovableWidgetMixin):
    settings = Settings()
    gap = 5
