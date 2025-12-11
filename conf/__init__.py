import os
from functools import lru_cache

from .base import AppSettings
from .deploy import DeploySettings
from .local import LocalSettings


APP_ENV_VAR = "APP_ENV"


@lru_cache
def get_application_settings() -> AppSettings:
    env = os.getenv(APP_ENV_VAR, "local").lower()

    if env == "deploy":
        settings_cls = DeploySettings
    else:
        settings_cls = LocalSettings

    return settings_cls()


setting = get_application_settings()