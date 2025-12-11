from conf import setting


def pytest_configure(config):
    # Force test environment for settings
    setting.DEBUG = False
    setting.APP_ENV = "test"
