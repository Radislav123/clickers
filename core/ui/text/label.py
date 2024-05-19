from core.service import Color
from core.settings import Settings
from core.texture import Texture
from core.ui.button import TextureButton


class Label(TextureButton):
    settings = Settings()

    DEFAULT_STYLE = {
        "normal": TextureButton.normal_style,
        "hover": TextureButton.hovered_style,
        "press": TextureButton.hovered_style,
        "disabled": TextureButton.normal_style
    }

    def __init__(self, **kwargs):
        if "color" not in kwargs:
            kwargs["color"] = Color.BACKGROUND
        if "width" not in kwargs:
            kwargs["width"] = 100
        if "height" not in kwargs:
            kwargs["height"] = 50
        if "texture" not in kwargs:
            kwargs["texture"] = Texture.create_empty(
                str(kwargs),
                (kwargs["width"], kwargs["height"]),
                kwargs["color"]
            )
        super().__init__(**kwargs)
