from core.view import View as CoreView
from simple.settings import Settings


class View(CoreView):
    settings = Settings()

    def __init__(self) -> None:
        super().__init__()
