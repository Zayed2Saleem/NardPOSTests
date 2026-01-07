# CI/CD Workflow Documentation

## 📄 File: `.github/workflows/qa-tests.yml`

This document explains the GitHub Actions workflow for NardPOS QA Automation.

---

## 🎯 Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    NardPOS QA Automation                        │
├─────────────────────────────────────────────────────────────────┤
│  Triggers: push (main/develop) | pull_request | manual          │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    ┌──────────────────┐            ┌──────────────────┐
    │   api-tests      │            │   ui-tests       │
    │   (Newman)       │            │   (Selenium)     │
    └────────┬─────────┘            └────────┬─────────┘
             │                               │
             ▼                               ▼
    ┌──────────────────┐            ┌──────────────────┐
    │ Upload API       │            │ Upload UI        │
    │ Report           │            │ Report +         │
    │                  │            │ Screenshots      │
    └────────┬─────────┘            └────────┬─────────┘
             │                               │
             └───────────────┬───────────────┘
                             ▼
                   ┌──────────────────┐
                   │    summary       │
                   │ (Test Results)   │
                   └──────────────────┘
```

---

## 🔧 Workflow Triggers

| Trigger | When It Runs |
|---------|--------------|
| `push` | On push to `main` or `develop` branches |
| `pull_request` | On PR to `main` branch |
| `workflow_dispatch` | Manual trigger from GitHub UI |

---

## 📋 Jobs Breakdown

### Job 1: `api-tests`

**Purpose:** Run API tests using Newman (Postman CLI)

| Step | Description |
|------|-------------|
| 1. Checkout | Clone the repository |
| 2. Setup Node.js | Install Node.js 18 |
| 3. Install Newman | Install Newman + Mockoon CLI |
| 4. Start Mock Server | Run Mockoon on port 3000 |
| 5. Run API Tests | Execute Postman collection |
| 6. Upload Report | Save HTML report as artifact |

**Artifacts Produced:**
- `api-test-report` → `reports/api-report.html`

---

### Job 2: `ui-tests`

**Purpose:** Run UI tests using Selenium + Python

| Step | Description |
|------|-------------|
| 1. Checkout | Clone the repository |
| 2. Setup Python | Install Python 3.11 |
| 3. Install Chrome | Install Google Chrome browser |
| 4. Install Dependencies | `pip install -r requirements.txt` |
| 5. Run UI Tests | Execute Pytest in headless mode |
| 6. Upload Report | Save HTML report as artifact |
| 7. Upload Screenshots | Save screenshots (on failure) |

**Artifacts Produced:**
- `ui-test-report` → `ui-tests/reports/`
- `screenshots` → `ui-tests/screenshots/` (only on failure)

---

### Job 3: `summary`

**Purpose:** Generate test results summary

- Runs after both `api-tests` and `ui-tests` complete
- Creates a summary table in GitHub Actions UI
- Shows pass/fail status for each job

---

## 🚀 How to Test the Workflow

### Method 1: Push to GitHub

```bash
# Navigate to project
cd /home/saleem/Documents/GitHub/qa-automation

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Add QA automation suite"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/nardpos-qa-case-study.git

# Push to main branch
git push -u origin main
```

**Result:** Workflow runs automatically on push.

---

### Method 2: Manual Trigger (GitHub UI)

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **NardPOS QA Automation** workflow
4. Click **Run workflow** button
5. Select branch and click **Run workflow**

---

### Method 3: Test Locally with `act`

[act](https://github.com/nektos/act) runs GitHub Actions locally using Docker.

```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Or on macOS
brew install act

# Run workflow locally
cd /home/hesham/Documents/GitHub/qa-automation
act push

# Run specific job
act push -j api-tests
act push -j ui-tests
```

**Requirements:**
- Docker must be installed and running
- First run downloads the runner image (~500MB)

---

## 📊 Viewing Results

### In GitHub Actions UI

1. Go to **Actions** tab in your repository
2. Click on the workflow run
3. View job logs by clicking on each job
4. Download artifacts from the **Artifacts** section

### Artifacts Location

| Artifact | Contents |
|----------|----------|
| `api-test-report` | Newman HTML report |
| `ui-test-report` | Pytest HTML report |
| `screenshots` | Failure screenshots (if any) |

---

## 🔍 Understanding the YAML

```yaml
name: NardPOS QA Automation      # Workflow name shown in GitHub UI

on:                               # Triggers
  push:
    branches: [main, develop]     # Run on push to these branches
  pull_request:
    branches: [main]              # Run on PR to main
  workflow_dispatch:              # Enable manual trigger

jobs:
  api-tests:                      # Job identifier
    runs-on: ubuntu-latest        # Runner OS
    steps:                        # Sequential steps
      - uses: actions/checkout@v4 # Predefined action
      - run: npm install ...      # Shell command

  ui-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'  # Action parameter

  summary:
    needs: [api-tests, ui-tests]  # Wait for these jobs
    if: always()                  # Run even if others fail
```

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow not running | Check branch name matches trigger |
| Chrome not found | Ensure Chrome install step runs first |
| Tests timeout | Increase timeout in pytest or workflow |
| Artifacts missing | Check `if: always()` on upload step |

---

## 📝 Environment Variables

| Variable | Used In | Purpose |
|----------|---------|---------|
| `HEADLESS=true` | ui-tests | Run browser without GUI |
| `$GITHUB_STEP_SUMMARY` | summary | Write to job summary |

---

## 🔗 Related Files

| File | Purpose |
|------|---------|
| `nardpos_api_mock.json` | Mockoon mock server config |
| `NardPOS_API_Collection.postman_collection.json` | API tests |
| `ui-tests/test_nardpos_e2e.py` | UI tests |
| `ui-tests/requirements.txt` | Python dependencies |
