from arcade.gui import UIBoxLayout, UIOnClickEvent

from core.service import Anchor
from core.texture import Texture
from core.ui.button import TextureButton
from core.ui.layout import BoxLayout
from core.ui.text import Label
from core.view import GameView as CoreGameView
from morel_buttons.view.view import View


class InfoBox(BoxLayout):
    auto_increment_label: TextureButton

    def __init__(self, view: "GameView", **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = view
        self.visible = False
        self.gap = 3

    def init(self) -> None:
        self.auto_increment_label = Label(text = self.view.get_displayed_auto_increment())
        self.add(self.auto_increment_label)

        self.fit_content()
        self.with_padding(all = self.gap)
        self.with_background(texture = Texture.create_rounded_rectangle(self.size, 2))
        self.move_to(self.view.info_button.right + 1, self.view.window.height - 1, Anchor.X.LEFT, Anchor.Y.TOP)


class InfoButton(TextureButton):
    def __init__(self, view: "GameView", **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = view

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.info_box.visible = not self.view.info_box.visible


class IncrementButton(TextureButton):
    def __init__(self, increment: int, view: "GameView", **kwargs) -> None:
        self.increment = increment
        self.view = view
        super().__init__(text = str(increment), **kwargs)

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.score += self.increment


class AutoIncrementButton(TextureButton):
    def __init__(self, auto_increment: int, view: "GameView", **kwargs) -> None:
        self.auto_increment = auto_increment
        self.view = view
        super().__init__(text = str(auto_increment), **kwargs)

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.auto_increment += self.auto_increment


class GameView(View, CoreGameView):
    score: float
    previous_displayed_score: str
    auto_increment: int
    previous_displayed_auto_increment: str
    default_increments = [1, 5, 10, 50]

    # время в секундах с начала игры
    time: float

    info_box: InfoBox
    info_button: InfoButton

    def reset_info(self) -> None:
        self.score = 0
        self.previous_displayed_score = self.get_displayed_score()
        self.auto_increment = 0
        self.previous_displayed_auto_increment = self.get_displayed_auto_increment()
        self.time = 0

    def prepare_increment_block(self) -> None:
        self.reset_info()
        label_kwargs = {
            "multiline": True,
            "width": 100,
            "height": 100
        }
        increment_label = Label(text = "Кнопки активного прироста", **label_kwargs)
        auto_increment_label = Label(text = "Кнопки пассивного прироста", **label_kwargs)

        increment_layout = UIBoxLayout(children = (increment_label,))
        auto_increment_layout = UIBoxLayout(children = (auto_increment_label,))
        layout = UIBoxLayout(
            vertical = False,
            children = (auto_increment_layout, increment_layout),
            space_between = 100
        )

        for increment in self.default_increments:
            button = IncrementButton(increment, self)
            increment_layout.add(button)

            auto_button = AutoIncrementButton(increment, self)
            auto_increment_layout.add(auto_button)

        layout.fit_content()
        layout.center_on_screen()
        self.ui_manager.add(layout)

    def prepare_info_block(self) -> None:
        self.info_box = InfoBox(self)

        self.info_button = InfoButton(self, text = self.get_displayed_score())
        self.info_button.move_to(0, self.window.height, Anchor.X.LEFT, Anchor.Y.TOP)
        self.ui_manager.add(self.info_button)

        self.info_box.init()
        self.ui_manager.add(self.info_box)

    def on_show_view(self) -> None:
        super().on_show_view()

        self.prepare_increment_block()
        self.prepare_info_block()

    def get_displayed_score(self) -> str:
        return str(int(self.score))

    def get_displayed_auto_increment(self) -> str:
        return str(self.auto_increment)

    def on_draw(self) -> None:
        if (score := self.get_displayed_score()) != self.previous_displayed_score:
            self.info_button.text = score
            self.previous_displayed_score = score
        if (self.info_box.visible and
                (auto_increment := self.get_displayed_auto_increment()) != self.previous_displayed_auto_increment):
            self.info_box.auto_increment_label.text = auto_increment
            self.previous_displayed_auto_increment = auto_increment
        super().on_draw()

    def on_update(self, delta_time: float) -> None:
        self.time += delta_time
        self.score += self.auto_increment * delta_time
