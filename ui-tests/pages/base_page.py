"""
NardPOS UI Automation - Base Page Object
Contains common methods used across all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver):
        """Initialize base page with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    def open(self, url):
        """Navigate to a URL."""
        self.driver.get(url)
        return self
    
    def find_element(self, locator):
        """Find a single element."""
        return self.driver.find_element(*locator)
    
    def find_elements(self, locator):
        """Find multiple elements."""
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        """Wait for element and click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return self
    
    def type_text(self, locator, text):
        """Wait for element and type text."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        return self
    
    def get_text(self, locator):
        """Get text from an element."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element.text
    
    def is_displayed(self, locator, timeout=5):
        """Check if element is displayed."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element(self, locator, timeout=15):
        """Wait for element to be visible."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=15):
        """Wait for element to be clickable."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def get_page_title(self):
        """Get the current page title."""
        return self.driver.title
    
    def get_current_url(self):
        """Get the current URL."""
        return self.driver.current_url
    
    def take_screenshot(self, filename):
        """Take a screenshot."""
        self.driver.save_screenshot(filename)
        return filename
    
    def scroll_to_element(self, locator):
        """Scroll to element."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return self
    
    def get_element_attribute(self, locator, attribute):
        """Get an attribute value from an element."""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def wait_for_text_in_element(self, locator, text, timeout=15):
        """Wait for specific text to appear in element."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))
    
    def execute_script(self, script, *args):
        """Execute JavaScript."""
        return self.driver.execute_script(script, *args)
