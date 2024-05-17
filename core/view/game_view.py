from arcade.gui import UIOnClickEvent

from core.service import Anchor
from core.ui.button import FlatButton
from core.view.view import View


class ExitButton(FlatButton):
    def __init__(self, view: "GameView", **kwargs) -> None:
        super().__init__(text = "Выход", **kwargs)

        self.view = view
        self.main_menu_view = self.view.window.main_menu_view

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.window.show_view(self.main_menu_view)


class GameView(View):
    exit_button: FlatButton

    def on_show_view(self) -> None:
        super().on_show_view()

        self.exit_button = ExitButton(self)
        self.exit_button.move_to(self.window.width, self.window.height, Anchor.X.RIGHT, Anchor.Y.TOP)
        self.ui_manager.add(self.exit_button)
