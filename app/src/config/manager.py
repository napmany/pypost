from functools import lru_cache

import os

from src.config.settings.base import BackendBaseSettings
from src.config.settings.development import BackendDevSettings
from src.config.settings.environment import Environment
from src.config.settings.production import BackendProdSettings


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> BackendBaseSettings:
        if self.environment == Environment.DEVELOPMENT.value:
            return BackendDevSettings()
        return BackendProdSettings()


@lru_cache()
def get_settings() -> BackendBaseSettings:
    environment = os.environ.get("ENVIRONMENT", "DEV")
    return BackendSettingsFactory(environment=environment)()
