from typing import Iterable, TYPE_CHECKING

from arcade.gui import UIOnClickEvent

from core.service import Anchor, Color
from core.texture import Texture
from core.ui.button import TextureButton
from core.ui.layout import BoxLayout
from morel_buttons.game_components.automation.logic import Logic
from morel_buttons.settings import Settings


if TYPE_CHECKING:
    from morel_buttons.view.game_view import GameView


class AutomationBox(BoxLayout):

    def __init__(self, logics: Iterable[Logic], view: "GameView", **kwargs) -> None:
        super().__init__(**kwargs)
        self.logics = list(logics)
        self.view = view
        self.visible = True

        self.automation_buttons: list["AutomationButton"] = []

    def init(self) -> None:
        for logic in self.logics:
            button = AutomationButton(logic, self.view)
            self.add(button)
            self.automation_buttons.append(button)

        self.fit_content()
        self.with_padding(all = self.gap)
        self.with_background(texture = Texture.create_rounded_rectangle(self.size))
        self.move_to(self.view.automation_box_button.right + 1, 0, Anchor.X.LEFT, Anchor.Y.DOWN)


class Button(TextureButton):
    settings = Settings()
    enabled: bool

    default_textures = {
        True: {
            "normal": Texture.create_rounded_rectangle(color = Color.STATE_ENABLED_NORMAL),
            "hover": Texture.create_rounded_rectangle(color = Color.STATE_ENABLED_HOVERED),
            "press": Texture.create_rounded_rectangle(color = Color.STATE_ENABLED_PRESSED),
            "disabled": Texture.create_rounded_rectangle(color = Color.STATE_ENABLED_DISABLED)
        },
        False: {
            "normal": Texture.create_rounded_rectangle(color = Color.STATE_DISABLED_NORMAL),
            "hover": Texture.create_rounded_rectangle(color = Color.STATE_DISABLED_HOVERED),
            "press": Texture.create_rounded_rectangle(color = Color.STATE_DISABLED_PRESSED),
            "disabled": Texture.create_rounded_rectangle(color = Color.STATE_DISABLED_DISABLED)
        },
        None: {
            "normal": Texture.create_rounded_rectangle(color = Color.STATE_INDETERMINATE_NORMAL),
            "hover": Texture.create_rounded_rectangle(color = Color.STATE_INDETERMINATE_HOVERED),
            "press": Texture.create_rounded_rectangle(color = Color.STATE_INDETERMINATE_PRESSED),
            "disabled": Texture.create_rounded_rectangle(color = Color.STATE_INDETERMINATE_DISABLED)
        }
    }

    def __init__(self, view: "GameView", **kwargs) -> None:
        self.view = view
        kwargs.update(self.get_textures_init())

        super().__init__(**kwargs)

    def get_textures_init(self) -> dict[str, Texture]:
        return {
            "texture": self.default_textures[self.enabled]["normal"],
            "texture_hovered": self.default_textures[self.enabled]["hover"],
            "texture_pressed": self.default_textures[self.enabled]["press"],
            "texture_disabled": self.default_textures[self.enabled]["disabled"]
        }

    def update_textures(self) -> None:
        self._textures = self.default_textures[self.enabled]


class AutomationButton(Button):
    def __init__(self, logic: Logic, view: "GameView", **kwargs) -> None:
        self.logic = logic
        super().__init__(view, **kwargs)

    def on_click(self, event: UIOnClickEvent) -> None:
        self.logic.change_state()
        self.update_textures()
        self.view.automation_box_button.update_textures()

    @property
    def enabled(self) -> bool:
        return self.logic.enabled


class AutomationBoxButton(Button):
    def on_click(self, event: UIOnClickEvent) -> None:
        self.view.automation_box.visible = not self.view.automation_box.visible

    @property
    def enabled(self) -> bool:
        enabled_buttons = sum(x.enabled for x in self.view.automation_box.automation_buttons)
        if enabled_buttons == len(self.view.automation_box.automation_buttons):
            state = True
        elif enabled_buttons == 0:
            state = False
        else:
            state = None

        return state
