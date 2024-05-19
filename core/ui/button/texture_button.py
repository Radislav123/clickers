import arcade
from arcade.gui import UITextureButton

from core.mixin import MovableWidgetMixin
from core.service import Color
from core.settings import Settings
from core.texture import Texture


class TextureButton(UITextureButton, MovableWidgetMixin):
    settings = Settings()
    DEFAULT_COLORS = {
        "texture": Color.NORMAL,
        "texture_hovered": Color.HOVERED,
        "texture_pressed": Color.PRESSED,
        "texture_disabled": Color.DISABLED
    }
    DEFAULT_STYLE = {
        "normal": UITextureButton.UIStyle(font_size = 12, font_name = settings.FONTS, font_color = Color.TEXT),
        "hover": UITextureButton.UIStyle(font_size = 14, font_name = settings.FONTS, font_color = Color.TEXT),
        "press": UITextureButton.UIStyle(font_size = 14, font_name = settings.FONTS, font_color = Color.TEXT),
        "disabled": UITextureButton.UIStyle(font_size = 12, font_name = settings.FONTS, font_color = Color.TEXT)
    }

    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            width: int = 100,
            height: int = 50,
            texture: arcade.Texture = None,
            **kwargs
    ) -> None:
        if texture is None:
            for texture_name, texture_color in self.DEFAULT_COLORS.items():
                size = (width, height)
                kwargs[texture_name] = Texture.create_rounded_rectangle(
                    size,
                    3,
                    texture_color,
                    Color.BORDER
                )

        super().__init__(
            x = x,
            y = y,
            width = width,
            height = height,
            **kwargs
        )
