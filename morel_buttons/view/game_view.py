from arcade.gui import UIBoxLayout, UIOnClickEvent

from core.ui.button import TextureButton
from core.view import GameView as CoreGameView
from morel_buttons.view.view import View


class IncrementButton(TextureButton):
    def __init__(self, increment: int, view: "GameView", **kwargs) -> None:
        self.increment = increment
        self.view = view
        super().__init__(text = str(increment), **kwargs)

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.score += self.increment
        print(self.view.score)


class GameView(View, CoreGameView):
    score: int

    def reset_info(self) -> None:
        self.score = 0

    def on_show_view(self) -> None:
        super().on_show_view()

        self.reset_info()
        default_increments = [1, 2, 5, 10, 50]
        layout = UIBoxLayout()
        for increment in default_increments:
            button = IncrementButton(increment, self)
            layout.add(button)

        layout.fit_content()
        layout.center_on_screen()
        self.ui_manager.add(layout)
