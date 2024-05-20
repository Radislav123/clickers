from typing import TYPE_CHECKING

from arcade.gui import UIOnClickEvent

from core.service import Anchor, Color
from core.texture import Texture
from core.ui.button import TextureButton
from core.ui.layout import BoxLayout
from core.ui.text import Label


if TYPE_CHECKING:
    from morel_buttons.view.game_view import GameView


class InfoBox(BoxLayout):
    total_score_label: Label
    auto_increment_label: Label

    def __init__(self, view: "GameView", **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = view
        self.visible = True

    def init(self) -> None:
        label_kwargs = {
            "color": Color.NORMAL,
            "width": 200,
            "height": 35
        }
        self.total_score_label = Label(text = self.view.displayed_total_score, **label_kwargs)
        self.add(self.total_score_label)

        self.auto_increment_label = Label(text = self.view.displayed_auto_increment, **label_kwargs)
        self.add(self.auto_increment_label)

        self.fit_content()
        self.with_padding(all = self.gap)
        self.with_background(texture = Texture.create_rounded_rectangle(self.size))
        self.move_to(self.view.info_button.right + 1, self.view.window.height - 1, Anchor.X.LEFT, Anchor.Y.TOP)


class InfoButton(TextureButton):
    def __init__(self, view: "GameView", **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = view

        self.move_to(0, self.view.window.height, Anchor.X.LEFT, Anchor.Y.TOP)

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.info_box.visible = not self.view.info_box.visible
