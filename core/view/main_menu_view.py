from arcade.gui import UIBoxLayout, UIOnClickEvent

from core.ui.button import TextureButton
from core.view.game_view import GameView
from core.view.menu_view import MenuView
from simple.view import GameView as SimpleGameView


class GameButton(TextureButton):
    def __init__(self, view: GameView, **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = view

    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.window.show_view(self.view)


class MainMenuView(MenuView):
    def __init__(self) -> None:
        super().__init__()

        self.app_views = (SimpleGameView(),)

    def construct_app_buttons(self) -> None:
        layout = UIBoxLayout()

        for view in self.app_views:
            button = GameButton(view, text = view.settings.app_name.capitalize())
            layout.add(button)

        layout.fit_content()
        layout.center_on_screen()
        self.ui_manager.add(layout)

    def on_show_view(self) -> None:
        super().on_show_view()

        self.construct_app_buttons()
