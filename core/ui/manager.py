import arcade.gui

from core.settings import Settings


class UIManager(arcade.gui.UIManager):
    settings = Settings()
