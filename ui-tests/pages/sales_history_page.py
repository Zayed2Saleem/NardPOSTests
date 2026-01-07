"""
NardPOS UI Automation - Sales History Page Object
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class SalesHistoryPage(BasePage):
    """Page object for Sales History page."""
    
    HISTORY_PAGE = (By.ID, "historyPage")
    HISTORY_TAB = (By.ID, "historyTab")
    SALES_TABLE_BODY = (By.ID, "salesTableBody")
    SALE_ROWS = (By.CLASS_NAME, "sale-row")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_history(self):
        self.click(self.HISTORY_TAB)
        return self
    
    def get_sales_count(self):
        rows = self.find_elements(self.SALE_ROWS)
        return len(rows)
    
    def get_all_sales(self):
        sales = []
        rows = self.find_elements(self.SALE_ROWS)
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 6:
                sales.append({
                    'receipt_number': cells[0].text,
                    'date': cells[1].text,
                    'items': cells[2].text,
                    'total': cells[3].text,
                    'payment': cells[4].text,
                    'status': cells[5].text
                })
        return sales
    
    def find_sale_by_receipt(self, receipt_number):
        for sale in self.get_all_sales():
            if receipt_number in sale['receipt_number']:
                return sale
        return None
    
    def is_sale_in_history(self, receipt_number):
        return self.find_sale_by_receipt(receipt_number) is not None
