from core.settings import Settings as CoreSettings


class Settings(CoreSettings):
    app_name = "simple"
    settings_path = f"{app_name}/settings.json"

    def __init__(self) -> None:
        super().__init__()
