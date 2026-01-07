# NardPOS QA Automation Case Study

A comprehensive QA automation suite for the NardPOS multi-tenant POS system, covering API testing, UI automation, and CI/CD integration.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Part 1 – API Automation](#part-1--api-automation)
- [Part 2 – UI Automation](#part-2--ui-automation)
- [Part 3 – CI/CD Integration](#part-3--cicd-integration)
- [Quick Start](#quick-start)
- [Test Credentials](#test-credentials)
- [Reports](#reports)

---

## 🎯 Overview

This project implements a complete QA automation framework for NardPOS, a multi-tenant SaaS POS platform. The solution includes:

| Component | Technology | Description |
|-----------|------------|-------------|
| API Testing | Mockoon + Postman/Newman | Mock API server with complete test collection |
| UI Testing | Selenium + Python + Pytest | End-to-end browser automation |
| CI/CD | GitHub Actions | Automated test pipeline |

---

## 📁 Project Structure

```
nardpos-qa-case-study/
│
├── 📄 README.md                           # This file
├── 📄 QA _ Automation Engineer NardPOS Case Study.pdf  # Original requirements
│
├── 🔌 API Testing (Part 1)
│   ├── nardpos_api_mock.json              # Mockoon mock server configuration
│   └── NardPOS_API_Collection.postman_collection.json  # Postman test collection
│
├── 🖥️ UI Testing (Part 2)
│   ├── mock-ui/
│   │   └── index.html                     # Mock NardPOS UI for testing
│   │
│   └── ui-tests/
│       ├── pages/                         # Page Object Model
│       │   ├── __init__.py
│       │   ├── base_page.py              # Base page with common methods
│       │   ├── login_page.py             # Login page object
│       │   ├── pos_page.py               # POS page object
│       │   └── sales_history_page.py     # Sales history page object
│       ├── screenshots/                   # Test screenshots
│       ├── reports/                       # HTML test reports
│       ├── conftest.py                   # Pytest fixtures & configuration
│       ├── test_nardpos_e2e.py           # Test cases
│       ├── requirements.txt              # Python dependencies
│       ├── .env.example                  # Environment config template
│       └── README.md                     # UI tests documentation
│
└── 🔄 CI/CD (Part 3)
    └── .github/
        └── workflows/
            └── qa-tests.yml              # GitHub Actions workflow
```

---

## 🔌 Part 1 – API Automation

### Endpoints Covered

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | POST | User authentication with JWT tokens |
| `/products` | GET | Retrieve product catalog |
| `/sales` | POST | Create a new sale |
| `/sales/:id` | GET | Get sale details by ID |
| `/sales/archive` | GET | Get archived sales list |

### Test Scenarios

#### Authentication (`/auth/login`)
- ✅ Valid credentials → 200 + JWT token
- ❌ Invalid username → 401 Unauthorized
- ❌ Wrong password → 401 Unauthorized
- ❌ Missing fields → 400 Bad Request

#### Products (`/products`)
- ✅ With valid Bearer token → 200 + product list
- ❌ Without token → 401 Unauthorized

#### Sales (`/sales`)
- ✅ Valid payload + token → 201 Created
- ❌ Without token → 401 Unauthorized
- ❌ Missing required fields → 400 Bad Request
- ❌ Empty items array → 400 Bad Request

#### Sales by ID (`/sales/:id`)
- ✅ Valid ID + token → 200 + sale details
- ❌ ID not found (99999) → 404 Not Found
- ❌ Invalid ID format → 400 Bad Request
- ❌ Without token → 401 Unauthorized

#### Archived Sales (`/sales/archive`)
- ✅ With token → 200 + archived sales list
- ❌ Without token → 401 Unauthorized

### Running API Tests

#### Option 1: Using Mockoon GUI
1. Download and install [Mockoon](https://mockoon.com/)
2. Import `nardpos_api_mock.json`
3. Start the mock server (runs on port 3000)
4. Import `NardPOS_API_Collection.postman_collection.json` into Postman
5. Run the collection

#### Option 2: Using Mockoon CLI + Newman
```bash
# Install tools
npm install -g @mockoon/cli newman newman-reporter-htmlextra

# Start mock server
mockoon-cli start --data nardpos_api_mock.json --port 3000

# Run tests (in another terminal)
newman run NardPOS_API_Collection.postman_collection.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/api-report.html
```

---

## 🖥️ Part 2 – UI Automation

### Technology Stack
- **Language:** Python 3.11+
- **Framework:** Selenium WebDriver
- **Test Runner:** Pytest
- **Pattern:** Page Object Model (POM)
- **Reporting:** pytest-html

### Test Cases

| Test Class | Test Name | Description |
|------------|-----------|-------------|
| `TestNardPOSEndToEnd` | `test_complete_sale_flow` | **E2E:** Login → Add 2 products → Checkout → Verify in history |
| `TestLogin` | `test_login_valid_credentials` | Login with valid credentials |
| `TestLogin` | `test_login_invalid_username` | Login with invalid username |
| `TestLogin` | `test_login_invalid_password` | Login with wrong password |
| `TestPOS` | `test_add_products_to_cart` | Add multiple products to cart |
| `TestPOS` | `test_checkout_button_disabled_empty_cart` | Verify checkout disabled when empty |
| `TestSalesHistory` | `test_sale_appears_in_history` | Verify completed sale in history |

### Running UI Tests

```bash
# Navigate to ui-tests directory
cd ui-tests

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Run all tests with HTML report
pytest test_nardpos_e2e.py -v --html=reports/report.html --self-contained-html

# Run only E2E tests
pytest test_nardpos_e2e.py -v -m e2e

# Run only smoke tests
pytest test_nardpos_e2e.py -v -m smoke

# Run in headless mode
HEADLESS=true pytest test_nardpos_e2e.py -v
```

### Page Objects

| Page | File | Key Methods |
|------|------|-------------|
| Base | `base_page.py` | `click()`, `type_text()`, `wait_for_element()` |
| Login | `login_page.py` | `login()`, `is_error_displayed()` |
| POS | `pos_page.py` | `add_product_to_cart()`, `click_checkout()` |
| History | `sales_history_page.py` | `is_sale_in_history()`, `get_all_sales()` |

---

## 🔄 Part 3 – CI/CD Integration

### GitHub Actions Workflow

The workflow runs on every push to `main` or `develop` branches:

```yaml
# .github/workflows/qa-tests.yml
name: NardPOS QA Automation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install Newman
        run: npm install -g newman newman-reporter-htmlextra @mockoon/cli
      - name: Start Mock Server
        run: mockoon-cli start --data nardpos_api_mock.json --port 3000 &
      - name: Wait for server
        run: sleep 5
      - name: Run API Tests
        run: newman run NardPOS_API_Collection.postman_collection.json --reporters cli,htmlextra
      - name: Upload API Report
        uses: actions/upload-artifact@v4
        with:
          name: api-test-report
          path: newman/

  ui-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Chrome
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable
      - name: Install Dependencies
        run: |
          cd ui-tests
          pip install -r requirements.txt
      - name: Run UI Tests
        run: |
          cd ui-tests
          HEADLESS=true pytest test_nardpos_e2e.py -v --html=reports/report.html
      - name: Upload UI Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: ui-test-report
          path: ui-tests/reports/
      - name: Upload Screenshots
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: screenshots
          path: ui-tests/screenshots/
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for API testing)
- Python 3.11+ (for UI testing)
- Google Chrome (for Selenium)

### 1. Clone & Setup
```bash
git clone <repository-url>
cd nardpos-qa-case-study
```

### 2. Run API Tests
```bash
# Install tools
npm install -g @mockoon/cli newman

# Start mock server
mockoon-cli start --data nardpos_api_mock.json --port 3000 &

# Run tests
newman run NardPOS_API_Collection.postman_collection.json
```

### 3. Run UI Tests
```bash
cd ui-tests
pip install -r requirements.txt
pytest test_nardpos_e2e.py -v --html=reports/report.html
```

---

## 🔐 Test Credentials

| Field | Value |
|-------|-------|
| Username | `test_user` |
| Password | `123456` |

---

## 📊 Reports

| Report Type | Location |
|-------------|----------|
| API Test Report | `newman/report.html` |
| UI Test Report | `ui-tests/reports/report.html` |
| Screenshots | `ui-tests/screenshots/` |

---

## 📝 Design Decisions

1. **Page Object Model (POM)**: Used for UI tests to improve maintainability and reusability
2. **Mockoon**: Chosen for API mocking due to its flexibility with response rules and templating
3. **Pytest**: Selected for its powerful fixtures, markers, and plugin ecosystem
4. **Environment Variables**: All configurations externalized for flexibility across environments

---

## 👤 Author

QA Automation Engineer Case Study Submission

---

## 📄 License

This project is for evaluation purposes only.
