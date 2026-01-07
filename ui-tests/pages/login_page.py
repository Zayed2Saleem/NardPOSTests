"""
NardPOS UI Automation - Login Page Object
Handles login page interactions.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Login page."""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    LOGIN_ERROR = (By.ID, "loginError")
    LOGIN_CONTAINER = (By.ID, "loginPage")
    LOGO = (By.CLASS_NAME, "logo")
    
    def __init__(self, driver):
        """Initialize login page."""
        super().__init__(driver)
    
    def is_login_page_displayed(self):
        """Check if login page is displayed."""
        return self.is_displayed(self.LOGIN_CONTAINER)
    
    def enter_username(self, username):
        """Enter username in the input field."""
        self.type_text(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password):
        """Enter password in the input field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        """
        Perform complete login flow.
        
        Args:
            username: Username to enter
            password: Password to enter
            
        Returns:
            self for method chaining
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self):
        """Get the error message text if displayed."""
        if self.is_error_displayed():
            return self.get_text(self.LOGIN_ERROR)
        return None
    
    def is_error_displayed(self):
        """Check if error message is displayed."""
        try:
            element = self.find_element(self.LOGIN_ERROR)
            return element.is_displayed() and element.value_of_css_property('display') != 'none'
        except:
            return False
    
    def get_page_title(self):
        """Get the page title."""
        return self.driver.title
    
    def is_logo_displayed(self):
        """Check if logo is displayed."""
        return self.is_displayed(self.LOGO)
