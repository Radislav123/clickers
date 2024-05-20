from arcade.gui import UIBoxLayout

from core.ui.text import Label
from core.view import GameView as CoreGameView
from morel_buttons.game_components.automation.logic import AutoClicker, AutoUpgrader
from morel_buttons.game_components.automation.ui import AutomationBox, AutomationBoxButton
from morel_buttons.game_components.increment import AutoIncrementButton, IncrementButton
from morel_buttons.game_components.info import InfoBox, InfoButton
from morel_buttons.view.view import View


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
    automation_box: AutomationBox
    automation_box_button: AutomationBoxButton

    auto_clicks: bool

    def reset_info(self) -> None:
        self.score = 0
        self.displayed_score = self.get_displayed_score()
        self.total_score = 0
        self.displayed_total_score = self.get_displayed_total_score()
        self.auto_increment = 0
        self.displayed_auto_increment = self.get_displayed_auto_increment()

        self.auto_clicks = False

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
        self.ui_manager.add(self.info_button)

        self.info_box.init()
        self.ui_manager.add(self.info_box)

    def prepare_automation(self) -> None:
        logics = [AutoClicker(), AutoUpgrader()]
        self.automation_box = AutomationBox(logics, self)

        self.automation_box_button = AutomationBoxButton(self)
        self.ui_manager.add(self.automation_box_button)

        self.automation_box.init()
        self.automation_box_button.update_textures()
        self.ui_manager.add(self.automation_box)

    def on_show_view(self) -> None:
        super().on_show_view()

        self.prepare_increment_block()
        self.prepare_info_block()
        self.prepare_automation()

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
