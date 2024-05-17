from arcade.gui import UIFlatButton, UIBoxLayout

from core.view.menu_view import MenuView
from simple.view import GameView as SimpleGameView


class MainMenuView(MenuView):
    def __init__(self) -> None:
        super().__init__()

        self.app_views = (SimpleGameView(),)
        self.construct_app_buttons()

    def construct_app_buttons(self) -> None:
        normal_style = UIFlatButton.UIStyle(bg = (58, 58, 78, 255))
        hovered_style = UIFlatButton.UIStyle(bg = (64, 64, 86, 255))
        pressed_style = UIFlatButton.UIStyle(bg = (40, 40, 60, 255))
        disabled_style = UIFlatButton.UIStyle(bg = (72, 72, 84, 255))
        style = {
            "normal": normal_style,
            "hover": hovered_style,
            "press": pressed_style,
            "disabled": disabled_style
        }

        layout = UIBoxLayout()

        for view in self.app_views:
            button = UIFlatButton(
                text = view.settings.app_name.capitalize(),
                style = style
            )
            layout.add(button)

        layout.fit_content()
        layout.center_on_screen()
        self.ui_manager.add(layout)
