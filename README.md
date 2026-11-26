# Laptop Price Scraper & Analysis

A Python project that scrapes laptop listings from an e-commerce website, cleans the data, and uses regression models to find out which specs affect price.

**Data source:** <SITE NAME>

## What it does

1. **Scraping** (`scraping.py`): Uses Selenium with `ThreadPoolExecutor` to scrape up to 50 laptops in parallel. Extracts name, current price, original price, discount status, RAM, SSD and screen size. Uses `WebDriverWait` for slow-loading pages and skips missing attributes without crashing. Saves raw data to `ultra_prices_50.xlsx`.
2. **Cleaning & statistics** (`stats_analysis.py`): Normalizes prices, RAM and SSD values, converts GB/TB units, and prints descriptive statistics (mean, median, standard deviation). Saves the result to `clean-data.xlsx`.
3. **Regression** (`regressions.py`): Compares three models for predicting price using R² scores:
   - Linear regression (SSD size)
   - Polynomial regression, degree 2 (SSD size)
   - Multiple linear regression (SSD, RAM, screen size)

## Results

Dataset: 50 laptops scraped from <SITE NAME>. Prices in <CURRENCY>.

| Model | R² |
|---|---|
| Linear regression (SSD) | 0.149 |
| Polynomial regression, degree 2 (SSD) | 0.184 |
| Multiple linear regression (SSD, RAM, screen size) | **0.251** |

**Key findings (multiple regression):**
- RAM has the strongest effect: each additional 1 GB of RAM is associated with roughly +39.6 in price.
- Each additional 1 GB of SSD is associated with roughly +0.70 in price.
- Screen size has a negative coefficient (-44.5), which is likely a small-sample and collinearity artifact rather than a real effect.

**Limitations:** Even the best model explains only about 25% of price variation. With 50 listings and three features, this is expected. Brand, CPU, GPU and discounts are not included and probably explain much of the remaining variance. Next steps: a larger sample and additional features.

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