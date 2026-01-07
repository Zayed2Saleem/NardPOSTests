# Selenium UI Automation Documentation

## 📄 NardPOS UI Test Suite

Complete UI automation framework using **Selenium WebDriver** with **Python** and **Pytest**.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Test Layer                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              test_nardpos_e2e.py                        │    │
│  │  • TestNardPOSEndToEnd (E2E flow)                       │    │
│  │  • TestLogin (authentication tests)                      │    │
│  │  • TestPOS (point of sale tests)                        │    │
│  │  • TestSalesHistory (history verification)              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Page Object Layer                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐     │
│  │  LoginPage   │ │   POSPage    │ │  SalesHistoryPage    │     │
│  │  • login()   │ │  • add_to_   │ │  • get_all_sales()   │     │
│  │  • is_error_ │ │    cart()    │ │  • find_sale_by_     │     │
│  │    displayed │ │  • checkout()│ │    receipt()         │     │
│  └──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘     │
│         └────────────────┼────────────────────┘                  │
│                          ▼                                       │
│              ┌─────────────────────┐                            │
│              │     BasePage        │                            │
│              │  • click()          │                            │
│              │  • type_text()      │                            │
│              │  • wait_for_element │                            │
│              └─────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Framework Layer                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   conftest.py   │  │  Selenium       │  │   Pytest        │  │
│  │   (Fixtures)    │  │  WebDriver      │  │   Framework     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Browser Layer                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │          Chrome / Firefox (Headless or GUI)             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ui-tests/
│
├── 📂 pages/                      # Page Object Model classes
│   ├── __init__.py               # Package init
│   ├── base_page.py              # Base class with common methods
│   ├── login_page.py             # Login page interactions
│   ├── pos_page.py               # POS page interactions
│   └── sales_history_page.py     # Sales history interactions
│
├── 📂 screenshots/                # Auto-captured screenshots
│   └── *.png                     # Test screenshots
│
├── 📂 reports/                    # Test reports
│   └── report.html               # HTML test report
│
├── 📄 conftest.py                # Pytest configuration & fixtures
├── 📄 test_nardpos_e2e.py        # Test cases
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env.example               # Environment template
└── 📄 README.md                  # This file
```

---

## 🔧 Setup & Installation

### Prerequisites

- Python 3.11 or higher
- Google Chrome or Firefox browser
- ChromeDriver or GeckoDriver (auto-managed by Selenium)

### Step 1: Install Dependencies

```bash
cd ui-tests
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings (optional)
nano .env
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `file:///.../mock-ui/index.html` | Application URL |
| `BROWSER` | `chrome` | Browser to use (`chrome` or `firefox`) |
| `HEADLESS` | `false` | Run without GUI (`true` or `false`) |
| `IMPLICIT_WAIT` | `10` | Implicit wait in seconds |
| `TEST_USERNAME` | `test_user` | Login username |
| `TEST_PASSWORD` | `123456` | Login password |

---

## 🚀 Running Tests

### Basic Commands

```bash
# Run all tests
pytest test_nardpos_e2e.py -v

# Run with HTML report
pytest test_nardpos_e2e.py -v --html=reports/report.html --self-contained-html

# Run in headless mode (no browser window)
HEADLESS=true pytest test_nardpos_e2e.py -v

# Run specific test class
pytest test_nardpos_e2e.py::TestLogin -v

# Run specific test
pytest test_nardpos_e2e.py::TestLogin::test_login_valid_credentials -v
```

### Using Test Markers

```bash
# Run only E2E tests
pytest test_nardpos_e2e.py -v -m e2e

# Run only smoke tests
pytest test_nardpos_e2e.py -v -m smoke

# Run only regression tests
pytest test_nardpos_e2e.py -v -m regression
```

### Parallel Execution

```bash
# Run tests in parallel (4 workers)
pytest test_nardpos_e2e.py -v -n 4
```

---

## 🧪 Test Cases

### TestNardPOSEndToEnd

| Test | Marker | Description |
|------|--------|-------------|
| `test_complete_sale_flow` | `@e2e`, `@smoke` | Full flow: Login → Add products → Checkout → Verify history |

### TestLogin

| Test | Marker | Description |
|------|--------|-------------|
| `test_login_valid_credentials` | `@smoke` | Login with valid credentials |
| `test_login_invalid_username` | `@regression` | Login with wrong username |
| `test_login_invalid_password` | `@regression` | Login with wrong password |

### TestPOS

| Test | Marker | Description |
|------|--------|-------------|
| `test_add_products_to_cart` | `@regression` | Add multiple products to cart |
| `test_checkout_button_disabled_empty_cart` | `@regression` | Verify checkout disabled when empty |

### TestSalesHistory

| Test | Marker | Description |
|------|--------|-------------|
| `test_sale_appears_in_history` | `@regression` | Verify completed sale in history |

---

## 📄 Page Objects Explained

### BasePage (`base_page.py`)

Base class with common Selenium operations:

```python
class BasePage:
    def click(self, locator)           # Wait and click element
    def type_text(self, locator, text) # Clear and type text
    def get_text(self, locator)        # Get element text
    def is_displayed(self, locator)    # Check visibility
    def wait_for_element(self, locator)# Explicit wait
    def take_screenshot(self, filename)# Capture screenshot
```

### LoginPage (`login_page.py`)

Handles login page interactions:

```python
class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    
    # Methods
    def login(self, username, password)  # Complete login flow
    def is_error_displayed()             # Check error message
    def get_error_message()              # Get error text
```

### POSPage (`pos_page.py`)

Handles POS page interactions:

```python
class POSPage(BasePage):
    # Methods
    def add_product_to_cart(product_id)  # Add product by ID
    def get_cart_item_count()            # Count cart items
    def select_payment_cash()            # Select cash payment
    def click_checkout()                 # Complete checkout
    def is_success_modal_displayed()     # Check success modal
    def get_receipt_number()             # Get receipt from modal
```

### SalesHistoryPage (`sales_history_page.py`)

Handles sales history page:

```python
class SalesHistoryPage(BasePage):
    # Methods
    def navigate_to_history()            # Click history tab
    def get_all_sales()                  # Get all sales as list
    def find_sale_by_receipt(receipt)    # Find specific sale
    def is_sale_in_history(receipt)      # Check if sale exists
```

---

## 📸 Screenshots

Screenshots are captured automatically:

1. **On test failure** - Captured by `conftest.py` hook
2. **During test steps** - Using `screenshot` fixture

### Screenshot Location

```
ui-tests/screenshots/
├── test_login_valid_credentials_login_success_20260106_184523.png
├── test_login_invalid_username_login_invalid_user_20260106_184525.png
├── test_add_products_to_cart_cart_with_products_20260106_184529.png
└── ...
```

### Taking Screenshots in Tests

```python
def test_example(self, driver, screenshot):
    # ... test steps ...
    screenshot('step_name')  # Saves: test_example_step_name_TIMESTAMP.png
```

---

## 📊 Reports

### HTML Report

Generated using `pytest-html`:

```bash
pytest test_nardpos_e2e.py --html=reports/report.html --self-contained-html
```

Report includes:
- Test results (pass/fail)
- Execution time
- Environment info
- Error messages and tracebacks

### Allure Report (Optional)

```bash
# Run with Allure
pytest test_nardpos_e2e.py --alluredir=reports/allure-results

# Generate report
allure serve reports/allure-results
```

---

## 🔍 Locator Strategies

### Recommended Priority

1. **ID** - Most reliable
2. **Name** - Good for forms
3. **CSS Selector** - Flexible and fast
4. **XPath** - Last resort, for complex cases

### Examples Used

```python
# By ID (preferred)
USERNAME_INPUT = (By.ID, "username")

# By Class Name
PRODUCT_CARDS = (By.CLASS_NAME, "product-card")

# By CSS Selector
CART_ITEM = (By.CSS_SELECTOR, ".cart-item")

# Dynamic locator
product_locator = (By.ID, f"product-{product_id}")
```

---

## ⏱️ Wait Strategies

### Implicit Wait

Set globally in `conftest.py`:

```python
browser.implicitly_wait(IMPLICIT_WAIT)  # Default: 10 seconds
```

### Explicit Wait

Used for specific conditions:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 15)
element = wait.until(EC.element_to_be_clickable(locator))
```

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `NoSuchDriverException` | Install Chrome/ChromeDriver or set `BROWSER=firefox` |
| `ElementNotInteractableException` | Add explicit wait before interaction |
| `StaleElementReferenceException` | Re-find the element after page change |
| Tests timeout | Increase `IMPLICIT_WAIT` in `.env` |
| Browser not opening | Set `HEADLESS=false` for debugging |

### Debug Mode

```bash
# Run single test with visible browser
HEADLESS=false pytest test_nardpos_e2e.py::TestLogin::test_login_valid_credentials -v -s
```

---

## 🔗 Related Files

| File | Purpose |
|------|---------|
| `../mock-ui/index.html` | Mock NardPOS application |
| `conftest.py` | Pytest fixtures and hooks |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment template |

---

## 📝 Writing New Tests

### Template

```python
import pytest
from pages.login_page import LoginPage
from pages.pos_page import POSPage

class TestNewFeature:
    
    @pytest.mark.regression
    def test_new_scenario(self, driver, base_url, test_credentials, screenshot):
        # Arrange
        login_page = LoginPage(driver)
        pos_page = POSPage(driver)
        
        # Act
        driver.get(base_url)
        login_page.login(test_credentials['username'], test_credentials['password'])
        screenshot('after_login')
        
        # Assert
        assert pos_page.is_dashboard_displayed()
```

### Best Practices

1. **Use Page Objects** - Don't use locators directly in tests
2. **One assertion per test** - Keep tests focused
3. **Use fixtures** - For setup/teardown
4. **Add markers** - For test categorization
5. **Take screenshots** - At key steps for debugging
