from core.settings import Settings as CoreSettings


class Settings(CoreSettings):
    app_name = "simple"

    def __init__(self) -> None:
        super().__init__()
