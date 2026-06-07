# Python WebDriver Framework

A production-grade Selenium WebDriver test framework using Python and pytest, demonstrating the Page Object Model pattern against [Sauce Demo](https://www.saucedemo.com).

## Features

- **Page Object Model** — clean separation between test logic and page interactions
- **Multi-browser support** — Chrome, Firefox, Edge via WebDriver Manager (no manual driver downloads)
- **Parallel execution** — `pytest-xdist` for faster feedback cycles
- **Automatic screenshot on failure** — captured and uploaded as CI artifacts
- **HTML & Allure reporting**
- **GitHub Actions CI** — runs on push/PR across Chrome and Firefox

## Project Structure

```
├── pages/              # Page Object classes
│   ├── base_page.py    # Shared wait/interaction helpers
│   ├── login_page.py
│   └── inventory_page.py
├── tests/
│   ├── conftest.py     # Fixtures: driver lifecycle, auth, failure screenshots
│   ├── test_login.py
│   └── test_inventory.py
├── utils/
│   └── driver_factory.py  # Browser instantiation abstraction
├── data/
│   └── test_data.json
└── .github/workflows/ci.yml
```

## Prerequisites

- Python 3.10+
- Chrome, Firefox, or Edge installed locally

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# Default (Chrome, headed)
pytest

# Headless Firefox
pytest --browser=firefox --headless

# Parallel execution across 4 workers
pytest -n 4

# Specific marker
pytest -m smoke

# With HTML report
pytest --html=reports/report.html --self-contained-html
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BROWSER` | `chrome` | `chrome`, `firefox`, `edge` |
| `HEADLESS` | `false` | `true` to run headless |
| `DEFAULT_TIMEOUT` | `10` | Explicit wait timeout in seconds |

## CI

GitHub Actions runs the full suite headlessly across Chrome and Firefox on every push and pull request, plus a nightly scheduled run. Artifacts (reports + failure screenshots) are retained for 7 days.
