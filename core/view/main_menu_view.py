from arcade.gui import UIBoxLayout

from core.ui.button import FlatButton
from core.view.menu_view import MenuView
from simple.view import GameView as SimpleGameView


class MainMenuView(MenuView):
    def __init__(self) -> None:
        super().__init__()

        self.app_views = (SimpleGameView(),)

    def construct_app_buttons(self) -> None:
        layout = UIBoxLayout()

        for view in self.app_views:
            button = FlatButton(text = view.settings.app_name.capitalize())
            button.on_click = lambda _: self.window.show_view(view)
            layout.add(button)

        layout.fit_content()
        layout.center_on_screen()
        self.ui_manager.add(layout)

    def on_show_view(self) -> None:
        super().on_show_view()

        self.construct_app_buttons()
