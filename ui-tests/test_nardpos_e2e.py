"""
NardPOS UI Automation - End-to-End Test Suite
Tests the complete POS flow: Login -> Create Sale -> Verify in History
"""

import pytest
import os
from pages.login_page import LoginPage
from pages.pos_page import POSPage
from pages.sales_history_page import SalesHistoryPage


class TestNardPOSEndToEnd:
    """End-to-end test suite for NardPOS."""
    
    @pytest.mark.e2e
    @pytest.mark.smoke
    def test_complete_sale_flow(self, driver, base_url, test_credentials, screenshot):
        """
        Test Case: Complete POS Sale Flow
        
        Steps:
        1. Login with valid credentials
        2. Add two products to cart
        3. Complete checkout
        4. Navigate to Sales History
        5. Verify the sale appears in history
        """
        # Initialize page objects
        login_page = LoginPage(driver)
        pos_page = POSPage(driver)
        history_page = SalesHistoryPage(driver)
        
        # Step 1: Open application and login
        driver.get(base_url)
        screenshot('01_login_page')
        
        assert login_page.is_login_page_displayed(), "Login page should be displayed"
        
        login_page.login(test_credentials['username'], test_credentials['password'])
        screenshot('02_after_login')
        
        # Verify dashboard is displayed
        assert pos_page.is_dashboard_displayed(), "Dashboard should be displayed after login"
        assert pos_page.get_welcome_username() == test_credentials['username']
        
        # Step 2: Add two products to cart
        pos_page.add_product_to_cart(1)  # Coca-Cola
        pos_page.add_product_to_cart(3)  # Lays Chips
        screenshot('03_products_added')
        
        # Verify cart has items
        assert pos_page.get_cart_item_count() == 2, "Cart should have 2 items"
        assert not pos_page.is_cart_empty(), "Cart should not be empty"
        
        # Step 3: Complete checkout
        pos_page.select_payment_cash()
        pos_page.click_checkout()
        screenshot('04_checkout_success')
        
        # Verify success modal
        assert pos_page.is_success_modal_displayed(), "Success modal should appear"
        receipt_number = pos_page.get_receipt_number()
        assert receipt_number.startswith('RCP-'), f"Receipt should start with RCP-, got: {receipt_number}"
        
        pos_page.close_success_modal()
        
        # Step 4: Navigate to Sales History
        history_page.navigate_to_history()
        screenshot('05_sales_history')
        
        # Step 5: Verify sale appears in history
        assert history_page.get_sales_count() >= 1, "Should have at least 1 sale"
        assert history_page.is_sale_in_history(receipt_number), \
            f"Sale {receipt_number} should appear in history"
        
        # Verify sale details
        sale = history_page.find_sale_by_receipt(receipt_number)
        assert sale is not None, "Sale should be found"
        assert 'Completed' in sale['status'], "Sale status should be Completed"
        
        screenshot('06_test_complete')
        print(f"\n✅ Test passed! Receipt: {receipt_number}")


class TestLogin:
    """Test suite for login functionality."""
    
    @pytest.mark.smoke
    def test_login_valid_credentials(self, driver, base_url, test_credentials, screenshot):
        """Test login with valid credentials."""
        login_page = LoginPage(driver)
        pos_page = POSPage(driver)
        
        driver.get(base_url)
        login_page.login(test_credentials['username'], test_credentials['password'])
        
        assert pos_page.is_dashboard_displayed()
        screenshot('login_success')
    
    @pytest.mark.regression
    def test_login_invalid_username(self, driver, base_url, screenshot):
        """Test login with invalid username."""
        login_page = LoginPage(driver)
        
        driver.get(base_url)
        login_page.login('invalid_user', '123456')
        
        assert login_page.is_error_displayed()
        screenshot('login_invalid_user')
    
    @pytest.mark.regression
    def test_login_invalid_password(self, driver, base_url, test_credentials, screenshot):
        """Test login with invalid password."""
        login_page = LoginPage(driver)
        
        driver.get(base_url)
        login_page.login(test_credentials['username'], 'wrong_password')
        
        assert login_page.is_error_displayed()
        screenshot('login_invalid_password')


class TestPOS:
    """Test suite for POS functionality."""
    
    @pytest.mark.regression
    def test_add_products_to_cart(self, driver, base_url, test_credentials, screenshot):
        """Test adding products to cart."""
        login_page = LoginPage(driver)
        pos_page = POSPage(driver)
        
        driver.get(base_url)
        login_page.login(test_credentials['username'], test_credentials['password'])
        
        # Add products
        pos_page.add_product_to_cart(1)
        pos_page.add_product_to_cart(2)
        pos_page.add_product_to_cart(3)
        
        assert pos_page.get_cart_item_count() == 3
        assert pos_page.is_checkout_enabled()
        screenshot('cart_with_products')
    
    @pytest.mark.regression
    def test_checkout_button_disabled_empty_cart(self, driver, base_url, test_credentials):
        """Test checkout button is disabled with empty cart."""
        login_page = LoginPage(driver)
        pos_page = POSPage(driver)
        
        driver.get(base_url)
        login_page.login(test_credentials['username'], test_credentials['password'])
        
        assert pos_page.is_cart_empty()
        assert not pos_page.is_checkout_enabled()


class TestSalesHistory:
    """Test suite for Sales History functionality."""
    
    @pytest.mark.regression
    def test_sale_appears_in_history(self, driver, base_url, test_credentials, screenshot):
        """Test that completed sale appears in history."""
        login_page = LoginPage(driver)
        pos_page = POSPage(driver)
        history_page = SalesHistoryPage(driver)
        
        driver.get(base_url)
        login_page.login(test_credentials['username'], test_credentials['password'])
        
        # Create a sale
        receipt = pos_page.create_sale_with_products([1, 4], 'card')
        
        # Check history
        history_page.navigate_to_history()
        
        assert history_page.is_sale_in_history(receipt)
        screenshot('sale_in_history')
