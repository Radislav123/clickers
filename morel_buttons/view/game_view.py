from arcade.gui import UIBoxLayout, UIOnClickEvent

from core.service import Anchor, Color
from core.texture import Texture
from core.ui.button import TextureButton
from core.ui.layout import BoxLayout
from core.ui.text import Label
from core.view import GameView as CoreGameView
from morel_buttons.view.view import View


class InfoBox(BoxLayout):
    total_score_label: Label
    auto_increment_label: Label

    def __init__(self, view: "GameView", **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = view
        self.visible = True
        self.gap = 5

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
        self.with_background(texture = Texture.create_rounded_rectangle(self.size, 2))
        self.move_to(self.view.info_button.right + 1, self.view.window.height - 1, Anchor.X.LEFT, Anchor.Y.TOP)


class InfoButton(TextureButton):
    def __init__(self, view: "GameView", **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = view

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.info_box.visible = not self.view.info_box.visible


class IncrementButton(TextureButton):
    def __init__(self, increment: float, view: "GameView", **kwargs) -> None:
        self.increment = increment
        self.view = view
        super().__init__(text = str(increment), **kwargs)

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.score += self.increment
        self.view.total_score += self.increment


class AutoIncrementButton(TextureButton):
    def __init__(self, auto_increment: float, view: "GameView", **kwargs) -> None:
        self.auto_increment = auto_increment
        self.upgrade_cost = self.auto_increment
        # увеличение цены улучшения после очередного улучшения
        self.upgrade_cost_coeff = 1.2
        self.view = view
        super().__init__(text = self.get_text(), **kwargs)

    def get_text(self) -> str:
        return f"{int(self.auto_increment)} ({int(self.upgrade_cost)})"

    def on_click(self, event: UIOnClickEvent) -> None:
        if self.view.score >= self.upgrade_cost:
            self.view.score -= self.upgrade_cost
            self.upgrade_cost *= self.upgrade_cost_coeff
            self.view.auto_increment += self.auto_increment

            self.text = self.get_text()


class GameView(View, CoreGameView):
    score: float
    displayed_score: str
    total_score: float
    displayed_total_score: str
    auto_increment: float
    displayed_auto_increment: str
    default_increments = [1, 5, 10, 50]

    info_box: InfoBox
    info_button: InfoButton

    def reset_info(self) -> None:
        self.score = 0
        self.displayed_score = self.get_displayed_score()
        self.total_score = 0
        self.displayed_total_score = self.get_displayed_total_score()
        self.auto_increment = 0
        self.displayed_auto_increment = self.get_displayed_auto_increment()

    def prepare_increment_block(self) -> None:
        self.reset_info()
        label_kwargs = {
            "multiline": True,
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
        return f"Счет: {int(self.score)}"

    def get_displayed_total_score(self) -> str:
        return f"Общий счет: {int(self.total_score)}"

    def get_displayed_auto_increment(self) -> str:
        return f"Пассивный доход: {int(self.auto_increment)}"

    def on_draw(self) -> None:
        if (score := self.get_displayed_score()) != self.displayed_score:
            self.info_button.text = score
            self.displayed_score = score
        if (total_score := self.get_displayed_total_score()) != self.displayed_total_score:
            self.info_box.total_score_label.text = total_score
            self.displayed_total_score = total_score
        if (self.info_box.visible and
                (auto_increment := self.get_displayed_auto_increment()) != self.displayed_auto_increment):
            self.info_box.auto_increment_label.text = auto_increment
            self.displayed_auto_increment = auto_increment
        super().on_draw()

    def on_update(self, delta_time: float) -> None:
        delta_score = self.auto_increment * delta_time
        self.score += delta_score
        self.total_score += delta_score
