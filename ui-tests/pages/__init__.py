"""
NardPOS UI Automation - Page Objects
Page Object Model (POM) pattern for maintainable test automation.
"""

from .base_page import BasePage
from .login_page import LoginPage
from .pos_page import POSPage
from .sales_history_page import SalesHistoryPage

__all__ = ['BasePage', 'LoginPage', 'POSPage', 'SalesHistoryPage']
