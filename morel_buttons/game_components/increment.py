from typing import TYPE_CHECKING

from arcade.gui import UIOnClickEvent

from core.ui.button import TextureButton


if TYPE_CHECKING:
    from morel_buttons.view.game_view import GameView


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
