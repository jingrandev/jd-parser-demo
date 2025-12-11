from .base import AppSettings


class TestSettings(AppSettings):
    """Settings for test environment."""

    DEBUG: bool = False
    APP_TITLE: str = "JD Parser API (Test)"
