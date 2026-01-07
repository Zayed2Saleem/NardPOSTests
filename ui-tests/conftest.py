"""
NardPOS UI Automation - Pytest Configuration
This file contains fixtures and hooks for the test suite.
"""

import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv('BASE_URL', 'file:///home/hesham/Documents/GitHub/qa-automation/mock-ui/index.html')
BROWSER = os.getenv('BROWSER', 'chrome').lower()
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
REPORT_DIR = os.path.join(os.path.dirname(__file__), 'reports')

# Ensure directories exist
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")


@pytest.fixture(scope="function")
def driver():
    """
    Create and configure WebDriver instance.
    Yields the driver and handles cleanup after test.
    """
    if BROWSER == 'firefox':
        options = FirefoxOptions()
        if HEADLESS:
            options.add_argument('--headless')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        browser = webdriver.Firefox(options=options)
    else:
        # Default to Chrome - use system chromedriver
        options = ChromeOptions()
        if HEADLESS:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        # Let Selenium find chromedriver automatically
        browser = webdriver.Chrome(options=options)

    browser.implicitly_wait(IMPLICIT_WAIT)
    browser.maximize_window()
    
    yield browser
    
    browser.quit()


@pytest.fixture(scope="function")
def base_url():
    """Return the base URL for tests."""
    return BASE_URL


@pytest.fixture(scope="function")
def test_credentials():
    """Return test credentials."""
    return {
        'username': os.getenv('TEST_USERNAME', 'test_user'),
        'password': os.getenv('TEST_PASSWORD', '123456')
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    Attaches screenshot to the HTML report.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_name = item.name.replace(' ', '_')
            screenshot_path = os.path.join(SCREENSHOT_DIR, f'{test_name}_{timestamp}.png')
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")


def pytest_html_report_title(report):
    """Set the title of the HTML report."""
    report.title = "NardPOS UI Automation Test Report"


@pytest.fixture(scope="function")
def screenshot(driver, request):
    """
    Fixture to take screenshots during tests.
    Usage: screenshot('step_name') in test
    """
    def _screenshot(name):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{request.node.name}_{name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        driver.save_screenshot(filepath)
        print(f"\n📸 Screenshot: {filepath}")
        return filepath
    
    return _screenshot
