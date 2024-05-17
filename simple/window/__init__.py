from core.window import Window as CoreWindow
from simple.settings import Settings


class Window(CoreWindow):
    settings = Settings()

    def __init__(self) -> None:
        super().__init__()
