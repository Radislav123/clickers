import dataclasses
import json

import os.path


@dataclasses.dataclass
class Window:
    width: int
    height: int


class Settings:
    app_name = "core"
    # нужно задавать статично, так как read_settings использует settings_path, для считывания настроек предков
    settings_path = f"{app_name}/settings.json"

    dynamic_modules = {
        "window": Window
    }
    window: dynamic_modules["window"]

    def __init__(self) -> None:
        self.read_settings()

    def read_settings(self) -> None:
        # noinspection PyTypeChecker
        mro: list[type[Settings]] = self.__class__.mro()[:-1]
        mro.reverse()
        for module_name, module_class in self.dynamic_modules.items():
            for ancestor in mro:
                if os.path.exists(ancestor.settings_path):
                    with open(ancestor.settings_path, 'r') as file:
                        settings_json = json.load(file)
                        if hasattr(self, module_name):
                            # обновляются настройки
                            setattr(
                                self,
                                module_name,
                                dataclasses.replace(getattr(self, module_name), **settings_json[module_name])
                            )
                        else:
                            # создается объект настроек впервые
                            setattr(self, module_name, module_class(**settings_json[module_name]))
