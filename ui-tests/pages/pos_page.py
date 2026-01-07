"""
NardPOS UI Automation - POS Page Object
Handles Point of Sale page interactions.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class POSPage(BasePage):
    """Page object for the POS (Point of Sale) page."""
    
    # Locators - Dashboard
    DASHBOARD = (By.ID, "dashboard")
    NAVBAR = (By.CLASS_NAME, "navbar")
    WELCOME_USER = (By.ID, "welcomeUser")
    TENANT_ID = (By.ID, "tenantId")
    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    
    # Locators - Navigation
    POS_TAB = (By.ID, "posTab")
    HISTORY_TAB = (By.ID, "historyTab")
    
    # Locators - Products
    PRODUCTS_GRID = (By.ID, "productsGrid")
    PRODUCT_CARDS = (By.CLASS_NAME, "product-card")
    
    # Locators - Cart
    CART_ITEMS = (By.ID, "cartItems")
    CART_ITEM = (By.CLASS_NAME, "cart-item")
    EMPTY_CART = (By.CLASS_NAME, "empty-cart")
    SUBTOTAL = (By.ID, "subtotal")
    TAX = (By.ID, "tax")
    TOTAL = (By.ID, "total")
    CHECKOUT_BUTTON = (By.ID, "checkoutBtn")
    
    # Locators - Payment
    CASH_BUTTON = (By.ID, "cashBtn")
    CARD_BUTTON = (By.ID, "cardBtn")
    MOBILE_BUTTON = (By.ID, "mobileBtn")
    
    # Locators - Success Modal
    SUCCESS_MODAL = (By.ID, "successModal")
    RECEIPT_NUMBER = (By.ID, "receiptNumber")
    RECEIPT_TOTAL = (By.ID, "receiptTotal")
    CLOSE_MODAL_BUTTON = (By.ID, "closeModal")
    
    def __init__(self, driver):
        """Initialize POS page."""
        super().__init__(driver)
    
    def is_dashboard_displayed(self):
        """Check if dashboard is displayed after login."""
        try:
            element = self.wait_for_element(self.DASHBOARD, timeout=10)
            return element.is_displayed()
        except:
            return False
    
    def get_welcome_username(self):
        """Get the username displayed in welcome message."""
        return self.get_text(self.WELCOME_USER)
    
    def get_tenant_id(self):
        """Get the tenant ID displayed."""
        return self.get_text(self.TENANT_ID)
    
    def click_logout(self):
        """Click the logout button."""
        self.click(self.LOGOUT_BUTTON)
        return self
    
    def click_pos_tab(self):
        """Click the POS tab."""
        self.click(self.POS_TAB)
        return self
    
    def click_history_tab(self):
        """Click the Sales History tab."""
        self.click(self.HISTORY_TAB)
        return self
    
    def get_product_count(self):
        """Get the number of products displayed."""
        products = self.find_elements(self.PRODUCT_CARDS)
        return len(products)
    
    def add_product_to_cart(self, product_id):
        """
        Add a product to cart by clicking on it.
        
        Args:
            product_id: The ID of the product (1-8)
        """
        product_locator = (By.ID, f"product-{product_id}")
        self.click(product_locator)
        time.sleep(0.3)  # Wait for cart update animation
        return self
    
    def add_product_by_index(self, index):
        """
        Add a product to cart by its index in the grid.
        
        Args:
            index: Zero-based index of the product
        """
        products = self.find_elements(self.PRODUCT_CARDS)
        if index < len(products):
            products[index].click()
            time.sleep(0.3)
        return self
    
    def get_cart_item_count(self):
        """Get the number of items in the cart."""
        items = self.find_elements(self.CART_ITEM)
        return len(items)
    
    def is_cart_empty(self):
        """Check if cart is empty."""
        return self.is_displayed(self.EMPTY_CART, timeout=2)
    
    def get_subtotal(self):
        """Get the subtotal amount."""
        return self.get_text(self.SUBTOTAL)
    
    def get_tax(self):
        """Get the tax amount."""
        return self.get_text(self.TAX)
    
    def get_total(self):
        """Get the total amount."""
        return self.get_text(self.TOTAL)
    
    def select_payment_cash(self):
        """Select cash payment method."""
        self.click(self.CASH_BUTTON)
        return self
    
    def select_payment_card(self):
        """Select card payment method."""
        self.click(self.CARD_BUTTON)
        return self
    
    def select_payment_mobile(self):
        """Select mobile payment method."""
        self.click(self.MOBILE_BUTTON)
        return self
    
    def click_checkout(self):
        """Click the checkout button to complete sale."""
        self.click(self.CHECKOUT_BUTTON)
        time.sleep(0.5)  # Wait for modal animation
        return self
    
    def is_checkout_enabled(self):
        """Check if checkout button is enabled."""
        button = self.find_element(self.CHECKOUT_BUTTON)
        return not button.get_attribute('disabled')
    
    def is_success_modal_displayed(self):
        """Check if success modal is displayed."""
        try:
            element = self.wait_for_element(self.SUCCESS_MODAL, timeout=5)
            style = element.get_attribute('style')
            return 'flex' in style or 'block' in style
        except:
            return False
    
    def get_receipt_number(self):
        """Get the receipt number from success modal."""
        text = self.get_text(self.RECEIPT_NUMBER)
        # Extract just the receipt number from "Receipt: RCP-XXXXXXXX-XXXX"
        if 'Receipt:' in text:
            return text.replace('Receipt:', '').strip()
        return text
    
    def get_receipt_total(self):
        """Get the total from success modal."""
        return self.get_text(self.RECEIPT_TOTAL)
    
    def close_success_modal(self):
        """Close the success modal."""
        self.click(self.CLOSE_MODAL_BUTTON)
        time.sleep(0.3)
        return self
    
    def create_sale_with_products(self, product_ids, payment_method='cash'):
        """
        Complete flow to create a sale with specified products.
        
        Args:
            product_ids: List of product IDs to add
            payment_method: Payment method ('cash', 'card', 'mobile')
            
        Returns:
            Receipt number from the completed sale
        """
        # Add products to cart
        for product_id in product_ids:
            self.add_product_to_cart(product_id)
        
        # Select payment method
        if payment_method == 'card':
            self.select_payment_card()
        elif payment_method == 'mobile':
            self.select_payment_mobile()
        else:
            self.select_payment_cash()
        
        # Complete checkout
        self.click_checkout()
        
        # Get receipt number
        receipt_number = self.get_receipt_number()
        
        # Close modal
        self.close_success_modal()
        
        return receipt_number
