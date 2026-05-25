import pytest
from utils.driver_manager import DriverManager
import time

@pytest.fixture(scope="function")
def driver():
    """每个测试用例的driver fixture"""
    driver = DriverManager.get_driver()
    yield driver
    DriverManager.quit_driver()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = DriverManager._driver
        if driver:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            driver.save_screenshot(f"screenshots/failed_{item.name}_{timestamp}.png")