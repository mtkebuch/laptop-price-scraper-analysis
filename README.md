# Laptop Price Scraper & Analysis

A Python project that scrapes laptop listings from an e-commerce website, cleans the data, and analyzes which specs affect price using regression models.

**Data source:** <SITE NAME>

## What it does

1. **Scraping** (`scraping.py`): Uses Selenium with `ThreadPoolExecutor` to scrape up to 50 laptops in parallel. Extracts name, current price, original price, discount status, RAM, SSD and screen size. Uses `WebDriverWait` for slow-loading pages and skips missing attributes without crashing. Saves raw data to `ultra_prices_50.xlsx`.
2. **Cleaning & statistics** (`stats_analysis.py`): Normalizes prices, RAM and SSD values, converts GB/TB units, and prints descriptive statistics (mean, median, standard deviation). Saves the result to `clean-data.xlsx`.
3. **Regression** (`regressions.py`): Compares three models for predicting price, using R² scores:
   - Linear regression (SSD size)
   - Multiple linear regression (SSD, RAM, screen size)
   - Polynomial regression (degree 2)

## How to run

Requires Python 3 and Google Chrome.

```bash
pip install -r requirements.txt
python scraping.py
python stats_analysis.py
python regressions.py
```

Run the scripts in this order: each one uses the output of the previous step.

## Tech stack

Python, Selenium, pandas, scikit-learn, openpyxl