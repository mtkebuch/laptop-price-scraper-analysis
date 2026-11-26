# Laptop Price Scraper & Analysis

A Python project that scrapes laptop listings from an e-commerce website, cleans the data, and uses regression models to find out which specs affect price.

**Data source:** [Ultra.ge](https://ultra.ge) (publicly available listings)

## What it does

1. **Scraping** (`scraping.py`): Uses Selenium with `ThreadPoolExecutor` to scrape up to 50 laptops. Extracts name, current price, original price, discount status, RAM, SSD and screen size. Fetches listing pages via pagination (no `limit`, `sort` or `filter` parameters), uses a small delay between requests, and runs only a few parallel browsers, in line with the site's robots.txt. Uses `WebDriverWait` for slow-loading pages and handles missing attributes without crashing. Saves raw data to `ultra_prices_50.xlsx`.
2. **Cleaning & statistics** (`stats_analysis.py`): Removes currency symbols and thousands separators from prices, strips units from RAM and SSD values, and prints descriptive statistics (mean, median, standard deviation) for current and original prices. Saves the result to `clean-data.xlsx`.
3. **Regression** (`regressions.py`): Converts SSD sizes from TB to GB and compares three models for predicting the original price using R² scores:
   - Linear regression (SSD size)
   - Polynomial regression, degree 2 (SSD size)
   - Multiple linear regression (SSD, RAM, screen size)

## Results

Dataset: 50 laptops scraped from Ultra.ge. Target variable: original price (before discount), in GEL. R² is computed on the full dataset (no train/test split). Data collected on 26 November 2026.

| Model | R² |
|---|---|
| Linear regression (SSD) | 0.149 |
| Polynomial regression, degree 2 (SSD) | 0.184 |
| Multiple linear regression (SSD, RAM, screen size) | **0.251** |

**Key findings (multiple regression):**
- RAM has the strongest effect: each additional 1 GB of RAM is associated with roughly +39.6 GEL in price.
- Each additional 1 GB of SSD is associated with roughly +0.70 GEL in price.
- Screen size has a negative coefficient (-44.5), which is likely a small-sample and collinearity artifact rather than a real effect.

**Limitations:** Even the best model explains only about 25% of price variation. With 50 listings and three features, this is expected. Brand, CPU, GPU and discounts are not included and probably explain much of the remaining variance. Because the models are evaluated on the same data they were trained on, R² is optimistic, and the more complex models have an inherent advantage in this comparison. A train/test split or cross-validation, a larger sample and additional features would give more reliable results.

## How to run

Requires Python 3 and Google Chrome.

```bash
pip install -r requirements.txt
python scraping.py
python stats_analysis.py
python regressions.py
```

Run the scripts in this order: each one uses the output of the previous step. Sample data files (`ultra_prices_50.xlsx`, `clean-data.xlsx`) are included in the repository. Prices change over time, so a fresh run may produce different numbers.

## Tech stack

Python, Selenium, pandas, scikit-learn, openpyxl